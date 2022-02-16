import json
from handler.RemoveDS import RemoveDS
from handler.RemoveJob import RemoveJob
from handler.Command.SendMsgCommand import SendMsgSuccessCommand, SendMsgFailCommand
from handler.Command.MsgReceiver import MsgReceiver
from constants.Errors import Errors
from urllib.parse import unquote


def finishingEventData(record):
    item = {}

    for field in list(record.keys()):
        value = record[field]
        v_k = list(value.keys())[0]
        item[field] = value[v_k]
    return item


def default():
    return None


__func_dict = {
    "insert:remove_DS": RemoveDS,
    "insert:remove_Job": RemoveJob
}


def run(eventName, jobCat, record):
    item = json.loads(unquote(json.dumps(finishingEventData(record)), "utf-8"))
    method = __func_dict.get(eventName + ":" + jobCat, default())
    if method is not None:
        try:
            print("Alex ==> \n")
            print(method)
            item["message"] = json.loads(item["message"])
            method().exec(item)

            SendMsgSuccessCommand(MsgReceiver()).execute({
                "data": item,
                "prefix": f"{jobCat}_"
            })
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
                }
            })
    else:
        print("未命中")
