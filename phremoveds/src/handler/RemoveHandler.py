import json
from handler.RemoveDS import RemoveDS
from handler.RemoveJob import RemoveJob
from handler.Command.SendMsgCommand import SendMsgSuccessCommand, SendMsgFailCommand
from handler.Command.MsgReceiver import MsgReceiver
from constants.Errors import Errors
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL


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
    logger = PhLogging().phLogger("Remover DS", LOG_DEBUG_LEVEL)
    item = finishingEventData(record)
    method = __func_dict.get(eventName + ":" + jobCat, default())
    if method is not None:
        try:
            logger.debug(f"Method ==>  {method} ")
            item["message"] = json.loads(item["message"])
            method().exec(item)

            SendMsgSuccessCommand(MsgReceiver()).execute({
                "data": item,
                "prefix": "remove_DS_"
            })
        except Errors as e:
            logger.debug(f"Error ====>  {e}")
            logger.debug(f"Item ===> {item}")
            SendMsgFailCommand(MsgReceiver()).execute({
                "data": item,
                "prefix": "remove_DS_",
                "error": {
                    "code": e.code,
                    "message": e.message,
                }
            })
    else:
        logger.debug("未命中")
