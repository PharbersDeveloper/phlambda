import os
import json
import time
import boto3
from datetime import datetime


def put_notification(runnerId, projectId, category, code, comments, date, owner, showName,
    jobCat='notification', jobDesc='executionSuccess', message='', status='gendag',
    dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    message = {
        "type": "operation",
        "opname": owner,
        "projectId": projectId,
        "cnotification": {
            "data": "{}",
            "error": "{}",
            "runId": runnerId
        }
    }

    table = dynamodb.Table('notification')
    response = table.put_item(
       Item={
            'id': runnerId,
            'projectId': projectId,
            'showName': showName,
            'status': status,
            'jobDesc': jobDesc,
            'comments': comments,
            'message': json.dumps(message, ensure_ascii=False),
            'jobCat': jobCat,
            'code': code,
            'category': category,
            'owner': owner
        }
    )
    return response


def lambda_handler(event, context):
    print(event)
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    smTemplateKey = event["dag"]
    stackName = event['runnerId'].replace("_", "-").replace(":", "-").replace("+", "-")
    # 1. put notification
    put_notification(event['runnerId'], event['projectId'], None, 0, "", int(ts), event['owner'], event['showName'])

    # 2. create state via cloudformation
    client = boto3.client('cloudformation')
    dagName = ("_").join(event['runnerId'].split("_")[:-1])
    response = client.create_stack(
        StackName=stackName, # event['runnerId'],
        TemplateURL='https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/jobs/statemachine/pharbers/template/steps-cfn.yaml',
        Parameters=[
            {
                'ParameterKey': 'StateMachineName',
                'ParameterValue': stackName #event['runnerId']
            },
            {
                'ParameterKey': 'S3Bucket',
                'ParameterValue': 'ph-platform'
            },
            {
                'ParameterKey': 'S3TemplateKey',
                'ParameterValue': smTemplateKey
             }
        ])
    print(response)

    # 3. sync the creation status
    while True:
        time.sleep(2)
        response = client.describe_stacks(
            StackName=stackName #  event['runnerId']
        )
        print(response)

        if len(response['Stacks']) > 0 and response['Stacks'][0]['StackStatus'] == 'CREATE_COMPLETE':
            break

        # TODO: Failed logic  AlreadyExistsException

    return 'arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:' + stackName # event['runnerId']
