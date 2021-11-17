import json
from phgetnumber.src.util.AWS.DynamoDB import DynamoDB


def lambda_handler(event, context):
    try:
        body = eval(event["body"])
        dynamodb = DynamoDB()
        result = dynamodb.getTableCount(body["tableName"], body["projectId"])
    except Exception as e:
        return {
            "statusCode": 503,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": {"message": str(e)}})
        }
    else:
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": result})
        }
