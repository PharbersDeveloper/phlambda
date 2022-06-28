import json
import boto3
from boto3.dynamodb.conditions import Key, Attr


dynamodb = boto3.resource("dynamodb")


def jupyterResourceCount(tenantId):
    result = dynamodb.Table("resource")
    result = result.scan(
        Select='COUNT',
        FilterExpression=Attr('tenantId').eq(tenantId) & (Attr("ctype").eq("jupyter") | Attr("ctype").eq("jupyter"))
    )
    return int(result.get("Count", 0))


def query_resource(tenantId):
    table = dynamodb.Table("resource")
    response = table.query(
        KeyConditionExpression=Key('tenantId').eq(tenantId),
    )
    return response.get("Items")


def lambda_handler(event, context):
    body = eval(event["body"])
    tenantId = body.get("tenantId")
    ownerId = body.get("ownerId")
    print(tenantId)
    try:
        if jupyterResourceCount(tenantId) <= 100:
            numbers = [i+1 for i in range(20, 100)]
            resources = query_resource(tenantId)
            owners = [resource_item for resource_item in resources if resource_item["owner"] == ownerId]
            prioritys = [int(resource_item.get('priority', 0)) for resource_item in resources]
            priority = min(list(set(numbers) - set(prioritys))) if prioritys else 0
            print(priority)
            if owners:
                result = {"code": 0, "message": "", "priority": priority, "exist": "true"}
            else:
                result = {"code": 0, "message": "", "priority": priority, "exist": "false"}
        else:
            raise Exception('jupyter count greater than 100')

    except Exception as e:
        result = {"code": 1, "message": str(e), "priority": "", "exist": ""}
    finally:
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(result)
        }
