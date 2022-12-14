import os
import json
import boto3
import traceback
import datetime
import math

'''
通用

args:
    event = {
        "traceId": "$.common.traceId",
        "projectId": "$.common.projectId",
        "owner": "$.common.owner",
        "showName": "$.common.showName",
        "jobCat": "$.action.cat",
        "jobDesc": "$.action.desc",
        "comments": "$.action.comments",
        "message": "$.result",
        "status": "failed"
    }
'''

def lambda_handler(event, context):
    print(event)
    result = {}

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('notification')

    response = table.put_item(
       Item={
            'id': event['traceId'],
            'projectId': event['projectId'],
            'date': math.floor(datetime.datetime.now().timestamp() * 1000),
            'jobCat': "notification",
            'jobDesc': event['jobDesc'],
            'comments': event['comments'],
            'message': json.dumps(event['message'], ensure_ascii=False),
            'code': 0,
            'owner': event['owner'],
            'showName': event['showName'],
            'traceId': event['traceId'],
            'status': event['status']
        }
    )
    print(response)

    return result
