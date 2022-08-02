import json
import boto3
from boto3.dynamodb.conditions import Key

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

