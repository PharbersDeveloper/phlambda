import json
import boto3
import uuid

dynamodb = boto3.resource("dynamodb")


def get_uuid():
    uu_id = uuid.uuid4()
    suu_id = ''.join(str(uu_id).split('-'))
    return suu_id


def lambda_handler(event, context):
    print(event)

    trigger = event.get("TriggerItem")[event.get("count")]
    common = event.get("common")

    args = {
        "common": {
            "tenantId": common["tenantId"],
            "traceId": get_uuid(),
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
