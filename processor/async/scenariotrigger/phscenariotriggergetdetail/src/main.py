import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
dynamodb = boto3.resource('dynamodb')

'''
需要通过scenarioId从dynamodb表scenario_step获取
当前scenarioId下的所有item并根据index排序返回details
args:
    event = {
            "iterator": {
                "index": 0,
                "currentStatus": "running"
            }
            "scenarioId": "ggjpDje0HUC2JW_f06f093f8f684289b949335e5e48edcd",
            "projectId": "ggjpDje0HUC2JW"
    }

return:
        "scenarioSteps": 
            {
                "detail": {
                    "type": "dataset",
                    "recursive": false, 
                    "ignore-error": false, 
                    "name": "1235"
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
    print(event)
    scenarioStep = {}
    # all_scenario_items = get_all_scenario_id_items(event["scenarioId"])
    currentIndex = event["iterator"]["index"]
    all_scenario_items = event["scenarioItems"]

    for scenario_step_item in all_scenario_items:
        if round(scenario_step_item.get("index")) == currentIndex:
            scenarioStep["detail"] = json.loads(scenario_step_item.get("detail"))
            scenarioStep["confData"] = scenario_step_item.get("confData")

    print(scenarioStep)

    # 'scenarioStep': {'detail': '{"type": "dataset", "recursive": false, "ignore-error": true, "name": "A1"}', 'confData': {}}

    return scenarioStep
