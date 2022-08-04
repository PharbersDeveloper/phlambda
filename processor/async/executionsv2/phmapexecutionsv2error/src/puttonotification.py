import json
import boto3
from boto3.dynamodb.conditions import Key

def put_notification(runnerId, projectId, category, code, comments, date, owner, showName, errorMessage,
                     jobCat='notification', jobDesc='executionFailed', status='failed', dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    message = {
        "type": "operation",
        "opname": owner,
        "projectId": projectId,
        "cnotification": {
            "data": "{}",
            "error": errorMessage,
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
            'date': date,
            'code': code,
            'category': category,
            'owner': owner
        }
    )
    return response

