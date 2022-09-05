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


def get_scenario(projectId, id):
    ds_table = dynamodb.Table('scenario')
    res = ds_table.query(
        KeyConditionExpression=Key("projectId").eq(projectId) & Key("id").eq(id)
    )
    return res.get("Items")[0]


def args_setting(projectId, scenarioId, codeFree, confData, **kwargs):
    confData = json.loads(confData)
    scenario_args: list = json.loads(get_scenario(projectId, scenarioId).get("args"))
    for key, value in confData.items():
        name = value[value.rfind("$")+1:]
        value = codeFree.get(name, "")
        if not value:
            value_list = [arg.get("default", "") for arg in scenario_args if arg.get("name") == name]
            value = value_list[0] if value_list else ""
        confData = {key: value} if value else {}
    return confData


def lambda_handler(event, context):
    print(event)
    scenarioStep = {}
    # all_scenario_items = get_all_scenario_id_items(event["scenarioId"])
    currentIndex = event["iterator"]["index"]
    all_scenario_items = event["scenarioItems"]

    for scenario_step_item in all_scenario_items:
        if round(scenario_step_item.get("index")) == currentIndex:
            scenarioStep["detail"] = json.loads(scenario_step_item.get("detail"))
            scenarioStep["confData"] = args_setting(confData=scenario_step_item.get("confData"), **event)
            scenarioStep["stepId"] = scenario_step_item.get("id")

    print(scenarioStep)

    # 'scenarioStep': {'detail': '{"type": "dataset", "recursive": false, "ignore-error": true, "name": "A1"}', 'confData': {}}

    return scenarioStep
