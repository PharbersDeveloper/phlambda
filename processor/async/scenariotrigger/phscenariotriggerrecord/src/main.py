import json
import boto3
import math
import datetime
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
dynamodb = boto3.resource('dynamodb')

'''
将错误提取出来写入到notification中
args:
    event = {
                "projectId": "ggjpDje0HUC2JW",
                "traceId": "",
                "projectName": "demo",
                "owner": "alfred",
                "showName": "alfred",
                "error": {
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
scenarioId
runnerId
date:
runtime:      manual / timer / dataset change
owner:
reporter
'''


def lambda_handler(event, context):

    ds_table = dynamodb.Table('scenario_execution')

    response = ds_table.put_item(
        Item={
            'scenarioId': event['scenarioId'],
            'runnerId': event['runnerId'],
            'date': math.floor(datetime.datetime.now().timestamp() * 1000),
            'runtime': event['runtime'],
            'owner': event['owner'],
            'reporter': event['reporter'],
            'traceId': event['traceId']
        }
    )

    return True
