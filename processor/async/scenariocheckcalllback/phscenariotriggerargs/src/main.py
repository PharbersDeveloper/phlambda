
import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal


dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    trigger = event.get("TriggerItem")[event.get("TriggerCount")]

    common = event.get("common")
    args = {
        "common": {
            "tenantId": common["runnerId"],
            "traceId": common["traceId"],
            "projectId": common["projectId"],
            "projectName": common["projectName"],
            "owner": common["owner"],
            "showName": common["showName"]
        },
        "action": {
            "cat": "scenarioTrigger",
            "desc": "scenarioTrigger",
            "comments": "",
            "message": "",
            "required": True
        },
        "notification": {
            "required": True
        },
        "scenario": {
            "scenarioId": trigger["scenarioId"],
            "runtime": "timer"
        }
    }
    return args
