import os
import json
import boto3
from datetime import datetime
from collections import deque
from cal import calDatasetPath
from args import *
from sms import *


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


def messageAdapter(x):
    x['ll'] = json.loads(x['cmessage'])
    return x


def lambda_handler(event, context):
    print(event)
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    dynamodb = boto3.resource('dynamodb')
    # 1. put notification
    put_notification(event['runnerId'], event['projectId'], None, 0, "", int(ts), event['owner'], event['showName'], dynamodb=dynamodb)
    
    # 2. generator execution args
    # TODO: create args and state machine files
    table = dynamodb.Table('dag')
    items = table.query(
        Select='ALL_ATTRIBUTES',
        Limit=1000,
        ExpressionAttributeValues={
            ':v1': event['projectId']
        },
        KeyConditionExpression='projectId=:v1'
    )['Items']

    datasets = list(filter(lambda x: x['ctype'] == 'node' and x['cat'] == 'dataset', items))
    jobs = list(filter(lambda x: x['ctype'] == 'node' and x['cat'] == 'job', items))
    links = list(filter(lambda x: x['ctype'] == 'link', items))
    links = list(map(messageAdapter, links))
    stackargs = deque()
    stacksm = deque()

    args = {}
    if (calDatasetPath(event['calculate']['name'], datasets, jobs, links, stackargs)):
        stack2smargs(stackargs, event, args)
        
    sm = {}
    if (calDatasetPath(event['calculate']['name'], datasets, jobs, links, stacksm)):
        prevJobName = 'StateMachineStartHook'
        stack2smdefs(stacksm, event, sm, prevJobName)
    
        s3 = boto3.client('s3')
        s3.put_object(
            Body=json.dumps(sm).encode(),
            Bucket='ph-max-auto',
            Key='2020-08-11/' + event['runnerId'] + '.json'
        )
        
        
    return {
        'args': args,
        'sm': 's3://ph-max-auto/2020-08-11/' + event['runnerId'] + '.json'
    }
    