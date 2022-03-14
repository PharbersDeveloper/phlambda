import json
from util.AWS.DynamoDB import DynamoDB


def lambda_handler(event, context):
    try:
        table = ["dagconf", "dataset", "dashboard"]
        body = eval(event["body"])
        dynamodb = DynamoDB()
        result = [dynamodb.getTableCount(i, body["projectId"]) for i in table]
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
            "body": json.dumps(dict(zip(table, result)))
        }
