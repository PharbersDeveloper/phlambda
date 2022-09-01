
import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
import time
from datetime import datetime
from decimal import Decimal


dynamodb = boto3.resource("dynamodb")
now_time = int(time.time())

# def make_time(strtime):
#     a = datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S').timetuple()
#     return int(time.mktime(a))


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


def put_item(items):
    for item in items:
        item["lastruntime"] = now_time
        dynamodb_table = dynamodb.Table("scenario_trigger")
        response = dynamodb_table.put_item(
            Item=item
        )


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
        FilterExpression=Attr("mode").eq("dataset")
    ).get("Items")
    return [trigger for trigger in response if list(set(json.loads(trigger.get("detail", {})).get("dsNames")) & set(names))]


def execution(projectId, name, **kwargs):
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
        triggers = triggers + query_trigger(id, names)

    put_item(triggers)
    return triggers


def upload_share(projectId, name):
    triggers = []
    for id in query_scenario(projectId):
        triggers += query_trigger(id, [name])
    return triggers


def timer():
    triggers = []
    period = {
        "minute": 60, "hour": 3600, "day": 86400, "week": 604800, "month": 2628000,
    }
    table = dynamodb.Table('scenario')
    scenario_response = table.scan(
        FilterExpression=Attr("mode").eq("dataset") & Attr("active").eq(True)
    )
    scenario_ids = [scenario.get("id") for scenario in scenario_response.get("Items")]
    table = dynamodb.Table('scenario_trigger')
    for scenarioid in scenario_ids:
        response = table.query(
            KeyConditionExpression=Key('scenarioId').eq(scenarioid),
            FilterExpression=Attr("mode").eq("timer")
        ).get("Items")
        triggers += [trigger for trigger in response if now_time >= int(trigger.get("lastruntime")) +
                     period[json.loads(trigger.get("detail", {})).get("period")] *
                     int(json.loads(trigger.get("detail", {})).get("value"))]

    return triggers


Command = {
    "execution": execution,
    "timer": timer,
    "upload": upload_share,
    "share": upload_share
}


def lambda_handler(event, context):
    print(event)
    mode = event.pop("type")
    item = Command[mode](**event)
    if not item:
        raise Exception("no scenario")

    return {
                "item": item,
                "count": len(item)
           }
