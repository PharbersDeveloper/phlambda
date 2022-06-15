import json
import boto3
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
                "errors": {
                }
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


def lambda_handler(event, context):
    print(event)
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
