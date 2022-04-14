import os
import json
import boto3
from datetime import datetime


def put_notification(runnerId, projectId, category, code, comments, date, owner, showName,  
    jobCat='notification', jobDesc='executionSuccess', message='', status='gendag',
    dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('notification')
    response = table.put_item(
       Item={
            'id': runnerId,
            'projectId': projectId,
            'showName': showName,
            'status': status,
            'jobDesc': jobDesc,
            'comments': comments,
            'message': message,
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

    stackName = event['runnerId'].replace("_", "-").replace(":", "-").replace("+", "-")
    # 1. put notification
    put_notification(event['runnerId'], event['projectId'], None, 0, "", int(ts), event['owner'], event['showName'])
    
    # 2. create state via cloudformation
    client = boto3.client('cloudformation')
    response = client.create_stack(
        StackName=stackName, # event['runnerId'],
        TemplateURL='https://ph-max-auto.s3.cn-northwest-1.amazonaws.com.cn/2020-08-11/steps-cfn.yaml',
        Parameters=[
            {
                'ParameterKey': 'StateMachineName',
                'ParameterValue': stackName #event['runnerId']
            },
            {
                'ParameterKey': 'S3Bucket',
                'ParameterValue': 'ph-max-auto'
            },
            {
                'ParameterKey': 'S3TemplateKey',
                'ParameterValue': '2020-08-11/' + event['runnerId'] + ".json"
             }
        ])
    print(response)

    # 3. sync the creation status
    while True:
        response = client.describe_stacks(
            StackName=stackName # event['runnerId']
        )
        print(response)
        
        if len(response['Stacks']) > 0 and response['Stacks'][0]['StackStatus'] == 'CREATE_COMPLETE':
            break

        # TODO: Failed logic  AlreadyExistsException
    
    return 'arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:' + stackName # event['runnerId']
