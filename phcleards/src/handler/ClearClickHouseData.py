import json
from constants.Errors import Errors
from handler.Command.SendMsgCommand import SendMsgSuccessCommand, SendMsgFailCommand
from handler.Command.SaveCommand import SaveCommand
from handler.Command.MsgReceiver import MsgReceiver
from handler.Command.ClearDSReceiver import ClearDSReceiver
from handler.Command.ClearCKReceiver import ClearCKReceiver
from clickhouse_driver.errors import Error


def finishingEventData(record):
    item = {}

    for field in list(record.keys()):
        value = record[field]
        v_k = list(value.keys())[0]
        item[field] = value[v_k]
    return item


def default(data):
    return None


__func_dict = {
    "insert:clear_DS_data": finishingEventData,
}


def run(eventName, jobCat, record):
    item = __func_dict.get(eventName + ":" + jobCat, default)(record)
    if item is not None:
        item["message"] = json.loads(item["message"])
        try:
            for message in item["message"]:
                SaveCommand(ClearCKReceiver()).execute({
                    "tableName": f"""{item["projectId"]}_{message["destination"]}""",
                    "version": message.get("version", "")
                })
                SaveCommand(ClearDSReceiver()).execute({
                    "dsid": message["dsid"]
                })
            SendMsgSuccessCommand(MsgReceiver()).execute({
                "data": item,
                "prefix": "clear_DS_"
            })

        except Error as e:
            SendMsgFailCommand(MsgReceiver()).execute({
                "data": item,
                "prefix": "clear_DS_",
                "error": {
                    "code": e.code,
                    "message": e.message,
                }
            })
        except Errors as e:
            print("Error ====> \n")
            print(e)
            SendMsgFailCommand(MsgReceiver()).execute({
                "data": item,
                "prefix": "clear_DS_",
                "error": {
                    "code": e.code,
                    "message": e.message,
                }
            })
        except Exception as e:
            print(e)
    else:
        print("未命中")
