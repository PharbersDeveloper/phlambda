import boto3
import time

'''
通用

args:
    event = {
        "traceId": "$.commom.traceId",
        "projectId": "$.common.projectId",
        "owner": "$.common.owner",
        "showName": "$.common.showName",
        "jobCat": "$.action.cat",
        "jobDesc": "$.action.desc",
        "comments": "$.action.comments",
        "required": "$.action.required"
    }
    
'''


def lambda_handler(event, context):
    print(event)
    result = {}

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('action')

    response = table.put_item(
       Item={
            'projectId': event['projectId'],
<<<<<<<<< Temporary merge branch 1
            'date': int(round(time.time() * 1000)),
=========
            'date': str(int(round(time.time() * 1000))),
>>>>>>>>> Temporary merge branch 2
            'jobCat': event['jobCat'],
            'jobDesc': event['jobDesc'],
            'comments': event['comments'],
            'message': event['message'],
            'code': 0,
            'owner': event['owner'],
            'showName': event['showName'],
            'traceId': event['traceId']
        }
    )
    print(response)

    return result
