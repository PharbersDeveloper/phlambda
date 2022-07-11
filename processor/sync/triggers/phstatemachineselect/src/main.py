import os
import json
import boto3
from datetime import datetime
from collections import deque
from cal import calDatasetPath
from selectcal import *

def messageAdapter(x):
    x['ll'] = json.loads(x['cmessage'])
    return x


def lambda_handler(event, context):
    event = json.loads(event["body"])
    print(event)
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    projectId = event['projectId']
    projectName = event['projectName']
    element = event['element']
    
    # 2. generator execution args
    # create args and state machine files
    dynamodb = boto3.resource('dynamodb')
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


    def jobsOutputDs(cur):
        cl = list(filter(lambda x: x['ll']['sourceName'] == cur['name'], links))[0]
        cds = list(filter(lambda x: x['name'] == cl['ll']['targetName'], datasets))[0]
        element['dataset'] = {
            'name': cds['name'],
            'represent-id': cds['representId']
        }


    if 'dataset' not in element and 'job' in element:
        jobsOutputDs(element['job'])


    stack = deque()
    args = []
    if (calDatasetPath(element['dataset']['name'], datasets, jobs, links, stack)):
        stack2smselect(stack, args, datasets, links)
        
    args.append(element['dataset']['represent-id'])
    result = {
        "calculate": element['dataset'],
        "selected": args
    }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(result)
    }
    