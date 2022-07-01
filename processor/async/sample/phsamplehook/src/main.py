import os
import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
# from phmetrixlayer import aws_cloudwatch_put_metric_data

def put_notification(runnerId, projectId, category, code, comments, date, owner, showName,  
    jobCat='notification', jobDesc='executionSuccess', message='', status='queued',
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
    res = table.query(
        KeyConditionExpression=Key("id").eq(runnerId)
                               & Key("projectId").begins_with(projectId)
    )
    if len(res["Items"]) == 0:
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
                'date': date,
                'code': code,
                'category': category,
                'owner': owner
            }
        )
    else:
        item = res["Items"][0]
        item.update({"status": status})
        response = table.put_item(Item=item)
    return response


# def put_metrics(runnerId, projectId, projectName, currentUserId, currentName, action="dag_execution_end"):
#     aws_cloudwatch_put_metric_data(projectId, projectName,
#                                     currentUserId,
#                                     currentName,
#                                     action,
#                                     runnerId, # action_detail,
#                                     1,
#                                     'Count')


def lambda_handler(event, context):
    # cicd 0701 1028
    print(event)
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    if event['stage'] == 'start':
        pid = event['projectId']
        pn = event['projectName']
        flowVersion = 'developer'

        # 1. put notification for dag
        put_notification(event['runnerId'], pid, None, 0, "", int(ts), event['owner'], event['showName'], status='running')
        # 2. put notification for every job
        for iter in event['Input'].keys():
            if iter == 'common':
                continue

            tmpJobName = '_'.join([pn, pn, flowVersion, iter])
            put_notification(event['runnerId'], tmpJobName, None, 0, "", int(ts), event['owner'], event['showName'])
        
    else:
        pid = event['projectId']
        # 1. put notification for dag
        put_notification(event['runnerId'], pid, None, 0, "", int(ts), event['owner'], event['showName'], status='success')
    
    return { "status": "ok"  }