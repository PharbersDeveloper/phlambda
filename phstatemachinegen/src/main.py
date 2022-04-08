import os
import json
import boto3
from datetime import datetime


def put_notification(runnerId, projectId, category, code, comments, date, owner, showName,  
    jobCat='notification', jobDesc='executionSuccess', message='', status='prepare',
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

    # 1. put notification
    put_notification(event['runnerId'], event['projectId'], None, 0, "", int(ts), event['owner'], event['showName'])
    
    # 2. generator execution args
    # TODO: create args and state machine files

    return {
        'args': 's3://ph-max-auto/2020-08-11/args.json',
        'sm': 's3://ph-max-auto/2020-08-11/steps-sm.json'
    }
