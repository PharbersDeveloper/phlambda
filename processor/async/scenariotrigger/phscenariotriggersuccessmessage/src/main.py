import json
import boto3
import time
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal

'''
将错误提取出来写入到notification中
args:
    event = {
                "projectId": "ggjpDje0HUC2JW",
                "traceId": "",
                "projectName": "demo",
                "owner": "alfred",
                "showName": "alfred",
            },
return:
    {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": errors
    }
}
'''

dynamodb = boto3.resource('dynamodb')


def put_item(item):
    dynamodb_table = dynamodb.Table("scenario_status")
    response = dynamodb_table.put_item(
        Item=item
    )


def query_status(projectId, traceId, **kwargs):
    scenario_status = dynamodb.Table("scenario_status")
    responses = scenario_status.query(
                IndexName='id-traceId-index',
                KeyConditionExpression=Key('id').eq(projectId) & Key('traceId').eq(traceId),
                ).get("Items")[0]
    responses["endAt"] = str(int(round(time.time()*1000)))
    responses["status"] = "success"
    return responses


def lambda_handler(event, context):
    print(event)
    put_item(query_status(**event))
    opname = event["owner"]
    message = {
        "type": "notification",
        "opname": opname,
        "cnotification": {
            "data": "{}",
            "error": "{}"
        }
    }
    return message
