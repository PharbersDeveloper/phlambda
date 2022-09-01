
import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
import time
from datetime import datetime
from decimal import Decimal


dynamodb = boto3.resource("dynamodb")

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
    return triggers, {}


def upload_share(projectId, name, **kwargs):
    triggers = []
    for id in query_scenario(projectId):
        triggers += query_trigger(id, [name])
    return triggers, {}


def timer(tenantId, **kwargs):
    triggers = []
    scenario_mapping = {}
    period = {
        "minute": 60, "hour": 3600, "day": 86400, "week": 604800, "month": 2628000,
    }
    table = dynamodb.Table('scenario')
    scenario_response = table.scan(
        FilterExpression=Attr("active").eq(True)
    ).get("Items")
    scenario_trigger = dynamodb.Table('scenario_trigger')
    for scenario in scenario_response:
        scenarioid = scenario.get("id")
        response = scenario_trigger.query(
            KeyConditionExpression=Key('scenarioId').eq(scenarioid),
            FilterExpression=Attr("mode").eq("timer")
        ).get("Items")
        add_trigger = [trigger for trigger in response if now_time >= int(trigger.get("lastruntime", 0)) +
                       period[json.loads(trigger.get("detail", {})).get("period")] *
                       int(json.loads(trigger.get("detail", {})).get("value"))]
        if add_trigger:
            scenario_mapping[scenarioid] = {"tenantId": tenantId,
                                            "projectId": scenario["projectId"],
                                            "projectName": scenario["projectName"],
                                            "owner": scenario["owner"],
                                            "showName": scenario["showName"]}
            triggers = triggers + add_trigger
    put_item(triggers)
    return triggers, scenario_mapping


Command = {
    "execution": execution,
    "timer": timer,
    "upload": upload_share,
    "share": upload_share
}


def lambda_handler(event, context):
    print(event)
    global now_time
    now_time = int(time.time())
    mode = event.pop("type")
    common = event.get("common")
    item, scenario_mapping = Command[mode](**common)
    if not item:
        raise Exception("no scenario")

    return {
                "item": item,
                "count": len(item),
                "scenario_mapping": scenario_mapping
           }
