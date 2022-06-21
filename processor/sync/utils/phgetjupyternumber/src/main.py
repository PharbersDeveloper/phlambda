import json
import boto3
from boto3.dynamodb.conditions import Key, Attr


dynamodb = boto3.resource("dynamodb", region_name="cn-northwest-1",
                          aws_access_key_id="AKIAWPBDTVEANKEW2XNC",
                          aws_secret_access_key="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")

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
    print(tenantId)
    try:
        if jupyterResourceCount(tenantId) <= 100:
            priority = max([resource_item.get('priority', 0) for resource_item in query_resource(tenantId)])
            print(priority)
            result = {"status": 1, "priority": int(priority)}
        else:
            raise Exception('jupyter count greater than 100')
    except Exception as e:
        result = {"status": 0, "priority": str(e)}
    finally:
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(result)
        }
