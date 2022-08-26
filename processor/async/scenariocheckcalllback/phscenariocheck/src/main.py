
import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal


dynamodb = boto3.resource("dynamodb")


def query_dag(projectId, name=None, **kwargs):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('dag')
    if name:
        res = table.query(
            IndexName='dag-projectId-name-index',
            KeyConditionExpression=Key("projectId").eq(projectId) & Key('name').eq(name),
        )
    else:
        res = table.query(
            KeyConditionExpression=Key("projectId").eq(projectId),
        )
    return res["Items"]


def query_scenario(projectId):
    table = dynamodb.Table('scenario')
    response = table.query(
        KeyConditionExpression=Key('projectId').eq(projectId),
    )
    return [scenario.get("id") for scenario in response.get("Items")]


def query_trigger(scenarioId, names):
    table = dynamodb.Table('scenario_trigger')
    response = table.query(
        KeyConditionExpression=Key('scenarioId').eq(scenarioId),
        filter=Attr("mode").eq("dataset")
    )
    return [trigger for trigger in response.get("Items") if trigger.get("detail", {}).get("dsNames") in names]


def execution(projectId, name):
    names = []
    triggers = []
    items = query_dag(projectId)
    job = query_dag(projectId, name)[0]
    representId = job["representId"]
    link_items = [link_item for link_item in items if link_item.get("ctype") == "link"]
    for link in link_items:
        cmessage = json.loads(link.get("cmessage"))
        targetName = cmessage.get("targetName")
        sourceId = cmessage.get("sourceId")
        if sourceId == representId:
            names.append(targetName)
    for id in query_scenario(projectId):
        triggers += query_trigger(id, names)
    return triggers


def upload_share(projectId, name):
    triggers = []
    for id in query_scenario(projectId):
        triggers += query_trigger(id, [name])
    return triggers


def timer():
    pass


Command = {
    "execution": execution,
    "timer": timer,
    "upload": upload_share,
    "share": upload_share
}


def lambda_handler(event, context):
    print(event)
    type = event.get("type")
    item = Command[type](**event)
    return {
                "item": item,
                "count": len(item)
           }
