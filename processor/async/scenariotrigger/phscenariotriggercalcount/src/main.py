import json
import boto3
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
'''


def get_all_scenario_id_items(scenarioId):
    ds_table = dynamodb.Table('scenario_step')
    res = ds_table.query(
        KeyConditionExpression=Key("scenarioId").eq(scenarioId)
    )
    return res.get("Items")


def lambda_handler(event, context):

    all_scenario_items = get_all_scenario_id_items(event["scenarioId"])
    count = len(all_scenario_items)

    return {
        "count": count,
        "scenarioItems": all_scenario_items
    }
