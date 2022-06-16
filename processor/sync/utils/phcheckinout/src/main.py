
import json
import boto3
from boto3.dynamodb.conditions import Key


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


class Check:

    def check_parameter(self ,projectId, name):
        item = query_dag(projectId, name)[0]
        representId = item["representId"]
        print(representId)
        if item["runtime"] != "intermediate":
            return "False"
        link_items = [link_item for link_item in query_dag(projectId) if link_item.get("ctype") == "link"]
        for link in link_items:
            cmessage = json.loads(link.get("cmessage"))
            targetId = cmessage.get("targetId")
            print(targetId)
            if targetId == representId:
                return "False"
        return "True"


def lambda_handler(event, context):
    body = eval(event["body"])
    print(body)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(Check().check_parameter(**body))
    }
