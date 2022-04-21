
import json
from Yarn import Yarn_Logs
from Step import Step_Logs
from AWS.DynamoDB import DynamoDB
from boto3.dynamodb.conditions import Key
from constants.Errors import DynamoDBNotItem, ItemLogsError, ItemTypeError


def query_data(projectId, jobIndex, **kwargs):
    dynamodb = DynamoDB()
    data = {
        "table_name": "execution",
        "expression": Key("projectId").eq(projectId) & Key("jobIndex").eq(jobIndex),
        "limit": 1000,
        "start_key": ""
    }
    return dynamodb.queryTable(data)["data"]


COMMANDS = {
    'lambdalog': None,
    'emrlog': None,
    'yarnlog': Yarn_Logs,
    'steplog': Step_Logs
}


def run(**kwargs):

    execution_msg = query_data(**kwargs)
    if not execution_msg:
        raise DynamoDBNotItem("DynamoDB Not find Item")

    try:
        logs_msg = json.loads(execution_msg.pop().get("logs"))
    except:
        raise ItemLogsError("item logs error")

    out_put = kwargs.get("out_put", [])
    if out_put and isinstance(out_put, list):
        out_put = [out.lower() for out in out_put]
        logs_msg = [logs for logs in logs_msg if logs["type"].lower() in out_put]

    log_data = ''
    for msg in logs_msg:
        command = msg.get("type", '').lower()
        if command not in COMMANDS.keys():
            raise ItemTypeError("Item Type Error")
        log_data += COMMANDS[command]().run(**msg)

    return log_data


def lambda_handler(event, context):
    try:
        data = run(**eval(event["body"]))
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": data, "status": 0}, ensure_ascii=False)
        }

    except Exception as e:
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": e.message, "status": e.code}, ensure_ascii=False)
        }
