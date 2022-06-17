
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
        items = query_dag(projectId)
        job = query_dag(projectId, name)[0]
        representId = job["representId"]
        target_names = []
        output_names = []

        link_items = [link_item for link_item in items if link_item.get("ctype") == "link"]
        input_names = [node_item["name"] for node_item in items if node_item.get("ctype") == "node" and node_item.get("cat") == "dataset"]
        intermediate_items = [link_item["name"] for link_item in items if link_item.get("runtime") == "intermediate"]

        for link in link_items:
            cmessage = json.loads(link.get("cmessage"))
            targetName = cmessage.get("targetName")
            sourceId = cmessage.get("sourceId")
            target_names.append(targetName)
            if sourceId == representId:
                output_names.append(targetName)

        output_names = output_names + list(set(intermediate_items).difference(set(target_names)))
        return input_names, output_names


def lambda_handler(event, context):
    body = eval(event["body"])
    print(body)
    input_names, output_names = Check().check_parameter(**body)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps({"input": input_names, "output": output_names})
    }
