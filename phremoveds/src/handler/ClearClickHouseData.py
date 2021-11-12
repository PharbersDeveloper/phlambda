import time
import http.client
import urllib.parse
from util.AWS.DynamoDB import DynamoDB
from boto3.dynamodb.conditions import Key, Attr

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


def executeSql(sql, type):
    conn = http.client.HTTPConnection(host="192.168.16.117", port="8123")
    # conn = http.client.HTTPSConnection(host="max.pharbers.com")
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


def cleanClickHouseData(tableName):
    sql = "DROP TABLE {0}".format(tableName)
    result = executeSql(sql, "POST")
    return 0 if result else 1


def removeDynamoDBData(tableName, id, projectId):
    dynamodb.deleteData({
        "table_name": tableName,
        "conditions": {
            "id": id,
            "projectId": projectId,
        }
    })
    return 1


def updateActionData(tableName, id):
    result = dynamodb.queryTable({
        "table_name": tableName,
        "limit": 1000,
        "expression": Key('id').eq(id),
        "start_key": ""
    })["data"]
    if len(result) > 0:
        result[0]["jobDesc"] = "success"
        result[0]["date"] = int(round(time.time() * 1000))
        dynamodb.putData({
            "table_name": tableName,
            "item": result[0]
        })
    return 1


def default(data):
    return None


__func_dict = {
    "insert:remove_DS": finishingEventData,
}


def run(eventName, jobCat, record):
    item = __func_dict.get(eventName + ":" + jobCat, default)(record)
    if item is not None:
        message = finishingEventData(item["message"])
        print(item)
        result = cleanClickHouseData(message["destination"]) & \
        removeDynamoDBData("dataset", message["dsid"], item["projectId"]) & \
        updateActionData("action", item["id"])
        print(result)
