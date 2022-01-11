import os
import json
import time
import constants.DefinValue as DV
from handler.Strategy.Reader import Reader
from handler.Command.MsgReceiver import MsgReceiver
from handler.Command.SendMsgCommand import SendMsgSuccessCommand, SendMsgFailCommand
from handler.Command.ActionReceiver import ActionReceiver
from handler.Command.SaveCommand import SaveActionCommand
from handler.Command.LockReceiver import LockReceiver
from handler.Command.LockCommand import LockCommand, UnLockCommand, WatchLockCommand
from handler.Command.RollBackCommand import RollBackCommand
from constants.Errors import Errors, ResourceBusy
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL


def lambda_handler(event, context):
    logger = PhLogging().phLogger("import data to ds", LOG_DEBUG_LEVEL)
    records = event["Records"]
    history = {}
    try:
        data = []
        for record in records:
            if record["eventName"].lower() != "insert":
                continue

            new_image = record["dynamodb"]["NewImage"]
            if record["eventName"].lower() == "insert" and \
                    new_image.get("jobCat", {"S": "None"})["S"] == "project_file_to_DS":
                item = {}
                for field in list(new_image.keys()):
                    value = new_image[field]
                    v_k = list(value.keys())[0]
                    item[field] = value[v_k]
                data.append(item)

                for item in data:
                    item["message"] = json.loads(item["message"])
                    history = dict({}, **item)
                    check_key = os.environ[DV.CHECK_APP_NAME] + "_" + item["projectId"] + "_" + item["message"]["destination"]
                    if WatchLockCommand(LockReceiver()).execute({"key": check_key}):
                        raise ResourceBusy("Resources Are Busy")

                    # TODO：这里会有lock会被别的操作者给释放掉，锁的内容与结构需要在这版本之后重新调整
                    # 触发条件: 当操作同一个DS一个大数据量另一个小数据量，小数据量先写完这样就会把lock去掉
                    lock_key = os.environ[DV.LOCK_APP_NAME] + "_" + item["projectId"] + "_" + item["message"]["destination"]
                    LockCommand(LockReceiver()).execute({
                        "key": lock_key,
                        "value": int(round(time.time() * 1000)),
                        "time": 60 * 60
                    })
                    result = Reader(item).reader()
                    item["jobDesc"] = "created"
                    SaveActionCommand(ActionReceiver()).execute(item)
                    SendMsgSuccessCommand(MsgReceiver()).execute(result)

    except Errors as e:
        logger.debug(e)
        history["jobDesc"] = "failed"
        RollBackCommand().execute(history)
        SaveActionCommand(ActionReceiver()).execute(history)
        SendMsgFailCommand(MsgReceiver()).execute({
            "id": history["id"],
            "project_id": history["projectId"],
            "prefix": "project_file_to_DS_",
            "owner": history["owner"],
            "showName": history["showName"],
            "opgroup": history["message"]["opgroup"],
            "error": {
                "code": e.code,
                "message": e.message
            }
        })
    finally:
        if len(history) > 0:
            UnLockCommand(LockReceiver()).execute({
                "key": os.environ[DV.LOCK_APP_NAME] + "_" + history["projectId"] + "_" + history["message"]["destination"]
            })
