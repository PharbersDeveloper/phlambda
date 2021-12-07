import time
import json
from util.AWS.DynamoDB import DynamoDB
from boto3.dynamodb.conditions import Key
from handler.RemoveDS import RemoveDS
from handler.RemoveJob import RemoveJob

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


def finishingEventData(record):
    item = {}

    for field in list(record.keys()):
        value = record[field]
        v_k = list(value.keys())[0]
        item[field] = value[v_k]
    return item


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
                    "status": "remove_DS_{}".format(state),
                    "error": error
                }
            }),
            "owner": result[0]["owner"],
            "showName": result[0].get("showName", "")
        }
    })


def default():
    return None


__func_dict = {
    "insert:remove_DS": RemoveDS,
    "insert:remove_Job": RemoveJob
}


def run(eventName, jobCat, record):
    item = finishingEventData(record)
    method = __func_dict.get(eventName + ":" + jobCat, default())
    if method is not None:
        try:
            print("Alex ==> \n")
            print(method)
            message = json.loads(item["message"])
            result = method(dynamodb).exec(item, message)

            updateActionData("action", item["id"], "succeed")
            insertNotification(item["id"], "succeed", "")
            print(result)
        except Exception as e:
            print("error ====> \n")
            print(str(e))
            print(item)
            updateActionData("action", item["id"], "failed")
            insertNotification(item["id"], "failed", str(e))
    else:
        print("未命中")
