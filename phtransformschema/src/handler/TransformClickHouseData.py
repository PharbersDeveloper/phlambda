import json
import time

from util.AWS.DynamoDB import DynamoDB
from boto3.dynamodb.conditions import Key
from clickhouse_driver.errors import ServerException
from util.ClieckHouse import ClickHouse

dynamodb = DynamoDB()
# import base64
# from util.AWS.STS import STS
# from constants.Common import Common
#
# sts = STS().assume_role(
#     base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
#     "Ph-Back-RW"
# )
# dynamodb = DynamoDB(sts=sts)


def executeSql(sql):
    client = ClickHouse(host="192.168.16.117", port="9000").getClient()
    # client = ClickHouse(host="localhost", port="19000").getClient()
    result = client.execute(sql)
    return result


def finishingEventData(record):
    item = {}

    for field in list(record.keys()):
        value = record[field]
        v_k = list(value.keys())[0]
        item[field] = value[v_k]
    return item


# 修改ClickHouse中的Col的类型
def transformClickHouseSchema(projectId, data):
    schema = {}
    try:
        tableName = projectId + "_" + data["destination"]
        schemas = data["schema"]
        for item in schemas:
            schema = item
            sql = f"""ALTER TABLE default.`{tableName}` MODIFY COLUMN `{item["src"]}` {item["type"]}"""
            executeSql(sql)
    except ServerException as se:
        print("ServerException  ==> \n")
        print(se)
        print(se.code)
        if se.code == 341 or se.code == 50:
            raise Exception(f"column {schema['src']} cannot convert to {schema['type']}")
    except Exception as e:
        raise Exception(f"unknown error")


# 修改DynamoDB的DS中的Schema类型
def transformDataSetSchema(projectId, data):
    dsId = data["dsid"]
    result = dynamodb.queryTable({
        "table_name": "dataset",
        "limit": 1000,
        "expression": Key("id").eq(dsId) & Key("projectId").eq(projectId),
        "start_key": ""
    })["data"].pop()
    schema = json.loads(result["schema"])
    changeSchema = data["schema"]
    for item in changeSchema:
        res = list(filter(lambda x: x["src"] == item["src"], schema))
        if len(res) == 1:
            idx = schema.index(res.pop())
            schema.pop(idx)
            schema.insert(idx, item)
    result["schema"] = json.dumps(schema, ensure_ascii=False)
    dynamodb.putData({
        "table_name": "dataset",
        "item": result
    })


# 回滚对ClickHouse Col的类型修改
# todo 这块可能会有无限递归的风险
def rollBackType(dsId, projectId):
    result = dynamodb.queryTable({
        "table_name": "dataset",
        "limit": 1000,
        "expression": Key("id").eq(dsId) & Key("projectId").eq(projectId),
        "start_key": ""
    })["data"].pop()
    if result is not None:
        schema = json.loads(result["schema"])
        destination = result["name"]
        transformClickHouseSchema(projectId, {
            "schema": schema,
            "destination": destination
        })


def updateActionData(tableName, projectId, date, state):
    result = dynamodb.queryTable({
        "table_name": tableName,
        "limit": 1000,
        "expression": Key('projectId').eq(projectId) & Key("date").eq(date),
        "start_key": ""
    })["data"]
    if len(result) > 0:
        result[0]["jobDesc"] = state
        dynamodb.putData({
            "table_name": tableName,
            "item": result[0]
        })


def insertNotification(actionId, projectId, date, state, error):
    result = dynamodb.queryTable({
        "table_name": "action",
        "limit": 1000,
        "expression": Key('projectId').eq(projectId) & Key("date").eq(date),
        "start_key": ""
    })["data"]
    message = json.loads(result[0]["message"])
    dynamodb.putData({
        "table_name": "notification",
        "item": {
            "id": actionId,
            "projectId": result[0]["projectId"],
            "code": 0,
            "comments": "",
            "date": int(round(time.time() * 1000)),
            "jobCat": "notification",
            "jobDesc": state,
            "message": json.dumps({
                "type": "operation",
                "opname": result[0]["owner"],
                "opgroup": message.get("opgroup", "0"),
                "cnotification": {
                    "status": "transform_schema_{}".format(state),
                    "error": error
                }
            }),
            "owner": result[0]["owner"],
            "showName": result[0]["showName"]
        }
    })


def default(data):
    return None


__func_dict = {
    "insert:transform_schema": finishingEventData,
}


def run(eventName, jobCat, record):
    item = __func_dict.get(eventName + ":" + jobCat, default)(record)
    if item is not None:
        try:
            message = json.loads(item["message"])
            print("message ==> \n")
            print(message)
            print(type(message))
            transformClickHouseSchema(item["projectId"], message)
            transformDataSetSchema(item["projectId"], message)
            updateActionData("action", item["projectId"], item["date"], "succeed")
            insertNotification(item["id"], item["projectId"], item["date"], "succeed", "")

        except Exception as e:
            print("Error ====> \n")
            print(str(e))
            rollBackType(json.loads(item["message"])["dsid"], item["projectId"])
            updateActionData("action", item["projectId"], item["date"], "failed")
            insertNotification(item["id"], item["projectId"], item["date"], "failed", str(e))
    else:
        print("未命中")
