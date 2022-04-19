
import json
from Yran import Yran_Logs
from AWS.DynamoDB import DynamoDB
from boto3.dynamodb.conditions import Key
from constants.Errors import DynamoDBNotItem


def query_data(projectId, jobIndex):
    dynamodb = DynamoDB()
    data = {
        "table_name": "execution",
        "expression": Key("projectId").eq(projectId) & Key("jobIndex").eq(jobIndex),
        "limit": 1000,
        "start_key": ""
    }
    return dynamodb.queryTable(data)["data"]


COMMANDS = {
    'lambda': None,
    'emr': None,
    'yran': Yran_Logs,
}


def run(**kwargs):

    execution_msg = query_data(**kwargs)
    if not execution_msg:
        raise DynamoDBNotItem("DynamoDB Not find Item")

    logs_msg = json.loads(execution_msg.pop().get("logs"))
    return COMMANDS[logs_msg["type"]]().run(**logs_msg)


def lambda_handler(event, context):
    try:
        data = run(**eval(event["body"]))
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": data, "status": 1}, ensure_ascii=False)
        }

    except Exception as e:
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": e.message, "status": e.code}, ensure_ascii=False)
        }
