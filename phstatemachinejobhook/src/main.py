import os
import json
import boto3
from datetime import datetime
# from phmetrixlayer import aws_cloudwatch_put_metric_data

def put_notification(runnerId, projectId, category, code, comments, date, owner, showName,  
    jobCat='notification', jobDesc='executionSuccess', message='', status='success',
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


# def put_metrics(runnerId, projectId, projectName, currentUserId, currentName, action="dag_execution_end"):
#     aws_cloudwatch_put_metric_data(projectId, projectName,
#                                     currentUserId,
#                                     currentName,
#                                     action,
#                                     runnerId, # action_detail,
#                                     1,
#                                     'Count')


def lambda_handler(event, context):
    print(event)
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    pn = event['projectName']
    flowVersion = 'developer'
    tmpJobName = '_'.join([pn, pn, flowVersion, event['jobName']])
    status = event['status']

    # 1. put notification
    put_notification(event['runnerId'], tmpJobName, None, 0, "", int(ts), event['owner'], event['showName'], status = status)
    # 2. put metrics
    # put_metrics(event["runnerId"], pid, event['projectName'], event["owner"], event["showName"], action = hid)
    return { "status": "ok"  }