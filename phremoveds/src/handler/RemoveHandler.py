import json
from handler.RemoveDS import RemoveDS
from handler.RemoveJob import RemoveJob
from handler.Command.SendMsgCommand import SendMsgSuccessCommand, SendMsgFailCommand
from handler.Command.MsgReceiver import MsgReceiver
from constants.Errors import Errors


def finishingEventData(record):
    item = {}

    for field in list(record.keys()):
        value = record[field]
        v_k = list(value.keys())[0]
        item[field] = value[v_k]
    return item


# def updateActionData(tableName, id, state):
#     result = dynamodb.queryTable({
#         "table_name": tableName,
#         "limit": 1000,
#         "expression": Key('id').eq(id),
#         "start_key": ""
#     })["data"]
#     if len(result) > 0:
#         result[0]["jobDesc"] = state
#         result[0]["date"] = int(round(time.time() * 1000))
#         dynamodb.putData({
#             "table_name": tableName,
#             "item": result[0]
#         })
# def insertNotification(actionId, state, error):
#     result = dynamodb.queryTable({
#         "table_name": "action",
#         "limit": 1000,
#         "expression": Key('id').eq(actionId),
#         "start_key": ""
#     })["data"]
#     message = json.loads(result[0]["message"])
#     dynamodb.putData({
#         "table_name": "notification",
#         "item": {
#             "id": actionId,
#             "projectId": result[0]["projectId"],
#             "code": 0,
#             "comments": "",
#             "date": int(round(time.time() * 1000)),
#             "jobCat": "notification",
#             "jobDesc": state,
#             "message": json.dumps({
#                 "type": "operation",
#                 "opname": result[0]["owner"],
#                 "opgroup": message[0].get("opgroup", "0"),
#                 "cnotification": {
#                     "status": "remove_DS_{}".format(state),
#                     "error": error
#                 }
#             }),
#             "owner": result[0]["owner"],
#             "showName": result[0].get("showName", "")
#         }
#     })


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
            item["message"] = json.loads(item["message"])
            method().exec(item)

            SendMsgSuccessCommand(MsgReceiver()).execute({
                "data": item,
                "prefix": "remove_DS_"
            })
            # updateActionData("action", item["id"], "succeed")
            # insertNotification(item["id"], "succeed", "")
        except Errors as e:
            print("error ====> \n")
            print(e)
            print(item)
            SendMsgFailCommand(MsgReceiver()).execute({
                "data": item,
                "prefix": "remove_DS_",
                "error": {
                    "code": e.code,
                    "message": e.message,
                    "meta": e.meta
                }
            })
            # updateActionData("action", item["id"], "failed")
            # insertNotification(item["id"], "failed", json.dumps({
            #     "code": e.code,
            #     "message": e.message
            # }, ensure_ascii=False))
    else:
        print("未命中")
