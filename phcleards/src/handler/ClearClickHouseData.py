import os
import json
import time
import http.client
import urllib.parse
from util.AWS.DynamoDB import DynamoDB
from boto3.dynamodb.conditions import Key, Attr
from constants.Errors import Errors, ResourceBusy
from constants.Common import Common
from util.PhRedis import PhRedis
from util.GenerateID import GenerateID

dynamodb = DynamoDB()
redis = PhRedis(host=os.environ[Common.REDIS_HOST], port=os.environ[Common.REDIS_PORT]).getRedis()


# import base64
# from util.AWS.STS import STS
# from constants.Common import Common
#
# sts = STS().assume_role(
#     base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
#     "Ph-Back-RW"
# )
# dynamodb = DynamoDB(sts=sts)


def executeSql(sql, type):
    conn = http.client.HTTPConnection(host=os.environ[Common.CLICKHOUSE_HOST], port=os.environ[Common.CLICKHOUSE_PORT])
    url = urllib.parse.quote("/ch/?query=" + sql, safe=':/?=&')
    conn.request(type, url)
    res = conn.getresponse()
    return res.read().decode("utf-8")


def finishingEventData(record):
    item = {}

    for field in list(record.keys()):
        value = record[field]
        v_k = list(value.keys())[0]
        item[field] = value[v_k]
    return item


def cleanClickHouseData(tableName, version):
    sql = "ALTER TABLE `{0}` DELETE WHERE 1 = 1 {1}".format(tableName,
                                                            " and version = {0}".format(version) if version else "")
    print("Alex Sql \n")
    print(sql)
    result = executeSql(sql, "POST")
    return 0 if result else 1


def cleanDynamoDBDSData(tableName, id):
    result = dynamodb.queryTable({
        "table_name": tableName,
        "limit": 1000,
        "expression": Key('id').eq(id),
        "start_key": ""
    })["data"]
    if len(result) > 0:
        result[0]["version"] = ""
        result[0]["date"] = int(round(time.time() * 1000))
        dynamodb.putData({
            "table_name": tableName,
            "item": result[0]
        })
        return 1
    return 0


def updateActionData(tableName, id, state):
    result = dynamodb.queryTable({
        "table_name": tableName,
        "limit": 1000,
        "expression": Key('id').eq(id),
        "start_key": ""
    })["data"]
    if len(result) > 0:
        result[0]["jobDesc"] = state
        result[0]["date"] = int(round(time.time() * 1000))
        dynamodb.putData({
            "table_name": tableName,
            "item": result[0]
        })


def insertNotification(actionId, state, error):
    result = dynamodb.queryTable({
        "table_name": "action",
        "limit": 1000,
        "expression": Key('id').eq(actionId),
        "start_key": ""
    })["data"]
    print("Alex ====>>>>> \n")
    print(actionId)
    print(result)
    print(result[0]["message"])
    print(type(result[0]["message"]))
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
                    "status": "clear_DS_{}".format(state),
                    "error": error
                }
            }),
            "owner": result[0]["owner"],
            "showName": result[0].get("showName", "")
        }
    })


def default(data):
    return None


__func_dict = {
    "insert:clear_DS_data": finishingEventData,
}


def run(eventName, jobCat, record):
    item = __func_dict.get(eventName + ":" + jobCat, default)(record)
    if item is not None:
        message = json.loads(item["message"])
        print("message ==> \n")
        print(message)
        print(type(message))
        check_key = os.environ[Common.CHECK_APP_NAME] + "_" + item["projectId"] + "_" + message["destination"]
        set_key = os.environ[Common.LOCK_APP_NAME] + "_" + item["projectId"] + "_" + message["destination"]
        try:
            if redis.exists(check_key):
                raise ResourceBusy("Resources Are Busy")
            else:
                if redis.setnx(set_key, int(round(time.time() * 1000))):
                    redis.expire(set_key, 60)

                result = cleanClickHouseData(item["projectId"] + "_" + message["destination"], message["version"]) & \
                         cleanDynamoDBDSData("dataset", message["dsid"])
                updateActionData("action", item["id"], "succeed")
                insertNotification(item["id"], "succeed", "")

                print(result)
        except Errors as e:
            print("Error ====> \n")
            print(e)
            updateActionData("action", item["id"], "failed")
            insertNotification(item["id"], "failed", json.dumps({
                "code": e.code,
                "message": e.message
            }, ensure_ascii=False))
        finally:
            redis.delete(set_key)
    else:
        print("未命中")
