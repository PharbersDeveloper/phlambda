from handler.Command.Receiver import Receiver
import constants.Common as Common
import json
import time
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL


class MsgReceiver(Receiver):

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]
        self.logger = PhLogging().phLogger("Message", LOG_DEBUG_LEVEL)

    def __update_action(self, status, data):
        action_item = dict({}, **data["data"])
        action_item["message"] = json.dumps(action_item["message"], ensure_ascii=False)
        action_item["jobDesc"] = status
        self.logger.debug(f"Action ====> {status}")
        self.dynamodb.putData({
            "table_name": "action",
            "item": action_item
        })

    def __send_notification(self, status, data):
        action_item = data["data"]
        message = action_item["message"][0]
        self.logger.debug(f"Notification ====> {message}")

        self.dynamodb.putData({
            "table_name": "notification",
            "item": {
                "id": action_item["id"],
                "projectId": action_item["projectId"],
                "code": "0",
                "comments": "",
                "date": int(round(time.time() * 1000)),
                "jobCat": "notification",
                "jobDesc": f"""{data["prefix"]}""",
                "message": json.dumps({
                    "type": "operation",
                    "opname": action_item["owner"],
                    "opgroup": message.get("opgroup", "-1"),
                    "cnotification": {
                        "status": f"""{data["jobCat"]}{status}""",
                        "data": json.dumps(message.get("data", {}), ensure_ascii=False),
                        "error": json.dumps(data.get("error", {}), ensure_ascii=False)
                    }
                }, ensure_ascii=False),
                "owner": action_item["owner"],
                "showName": action_item["showName"],
                "status": status
            }
        })

    def succeed(self, data):
        self.__update_action("succeed", data)
        self.__send_notification("succeed", data)

    def failed(self, data):
        self.__update_action("failed", data)
        self.__send_notification("failed", data)

