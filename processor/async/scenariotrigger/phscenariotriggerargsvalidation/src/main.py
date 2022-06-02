import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
'''
这个函数只做一件事情，检查参数是否合法
args:
    event = {
        "common": {
            "traceId": "alfred-resource-creation-traceId",
            "projectId": "ggjpDje0HUC2JW",
            "tenantId": "zudIcG_17yj8CEUoCTHg",
            "projectName": "demo",
            "owner": "alfred",
            "showName": "alfred"
        },
        "action": {
            "cat": "scenarioTrigger",
            "desc": "scenario trigger",
            "comments": "something need to say",
            "message": "something need to say",
            "required": true
        },
        "notification": {
            "required": true      
        },
        "scenario": {
            "scenarioId": "scenario id",       
        }
    }
'''


def get_item_from_dag(name, projectId):
    ds_table = dynamodb.Table('dag')
    res = ds_table.query(
        IndexName='dag-projectId-name-index',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("name").eq(name)
    )


def get_scenario_item_from_dynamodb(scenarioId):
    ds_table = dynamodb.Table('scenario_step')
    res = ds_table.query(
        KeyConditionExpression=Key("scenarioId").eq(scenarioId)
    )
    return res.get(res["Items"])


def check_parameter(event):

    # 1. common 必须存在
    if not event.get("common"):
        raise Exception('common must exist')

    # 2. action 必须存在cat 必须是 scenarioTrigger
    if not event.get("action"):
        raise Exception('action must exist')
    if not event["action"].get("cat") == "scenarioTrigger":
        raise Exception('action.cat must be scenarioTrigger')

    # 3. scenarioId 在 ScenarioStep 表中必须存在
    scenarioId = event["scenarioId"].get("scenarioId")
    scenarioItems = get_scenario_item_from_dynamodb(scenarioId)
    if len(scenarioItems) == 0:
        raise Exception('scenario step must exist')

    # 4. scenarioStep中 detail里的 name 必须在dag表中存在
    for scenarioItem in scenarioItems:
        ds_name = scenarioItem["detail"]["name"]
        get_item_from_dag(ds_name, event["common"]["projectId"])


    # 5. ssm 中必须存在 key 为 tenantId的项
    return True


def lambda_handler(event, context):

    return check_parameter(event)
    # 1. common 必须存在
    # 2. action 必须存在 cat 必须是 scenarioTrigger
    # 3. scenarioId 在 ScenarioStep 表中必须存在
    # 4. scenarioStep中 detail里的 name 必须在dag表中存在
    # 5. ssm 中必须存在 key 为 tenantId的项
