
import json
from Yarn import Yarn_Logs
from Step import Step_Logs
from AWS.DynamoDB import DynamoDB
from boto3.dynamodb.conditions import Key
from constants.Errors import DynamoDBNotItem, ItemLogsError, ItemTypeError


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

    step_log = ''
    data_list = []
    for msg in logs_msg:
        command = msg.get("type", '').lower()
        if command not in COMMANDS.keys():
            raise ItemTypeError("Item Type Error")
        result = COMMANDS[command]().run(**msg)
        if command == "steplog":
            step_log = result
        else:
            data_list.append(result)
    return [step_log + data for data in data_list]


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
