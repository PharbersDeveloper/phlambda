import os
import json
import boto3
from datetime import datetime
from phmetrixlayer import aws_cloudwatch_put_metric_data

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


def put_metrics(runnerId, projectId, projectName, currentUserId, currentName, action="dag_execution_end"):
    aws_cloudwatch_put_metric_data(projectId, projectName,
                                    currentUserId,
                                    currentName,
                                    action,
                                    runnerId, # action_detail,
                                    1,
                                    'Count')


def lambda_handler(event, context):
    print(event)
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    hook = event['hook']
    cat = event['cat']

    pid = None
    if cat == 'execute':
        pid = event['projectId'] 
    else:
        pid = event['jobName']

    hid = None
    if hook == 'start' and cat == 'execute':
        hid = "dag_execution_start"
    elif hook == 'end' and cat == 'execute':
        hid = "dag_execution_end"
    elif hook == 'start' and cat == 'step':
        hid = "dag_step_start"
    elif hook == 'end' and cat == 'step':
        hid = "dag_step_end"

    status = event['status']

    # 1. put notification
    put_notification(event['runnerId'], pid, None, 0, "", int(ts), event['owner'], event['showName'], status = status)
    # 2. put metrics
    put_metrics(event["runnerId"], pid, event['projectName'], event["owner"], event["showName"], action = hid)
    return { "status": "ok"  }