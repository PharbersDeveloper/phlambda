from handler.Command.Receiver import Receiver
import constants.Common as Common
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL
import json
import time


class MsgReceiver(Receiver):

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]
        self.logger = PhLogging().phLogger("Message", LOG_DEBUG_LEVEL)

    def __send_notification(self, status, message):
        self.logger.debug(f"Alex Notification ====> {status} \n {message}")
        self.dynamodb.putData({
            "table_name": "notification",
            "item": {
                "id": message["id"],
                "projectId": message["project_id"],
                "code": "0",
                "comments": "",
                "date": int(round(time.time() * 1000)),
                "jobCat": "notification",
                "jobDesc":  f"""{message["prefix"]}""",
                "message": json.dumps({
                    "type": "operation",
                    "opname": message["owner"],
                    "opgroup": message.get("opgroup", "-1"),
                    "cnotification": {
                        "status": f"""{message["jobCat"]}{status}""",
                        "data": json.dumps(message.get("data", {}), ensure_ascii=False),
                        "error": json.dumps(message.get("error", {}), ensure_ascii=False)
                    }
                }, ensure_ascii=False),
                "owner": message["owner"],
                "showName": message["showName"],
                "status": status
            }
        })

    def succeed(self, data):
        self.__send_notification("succeed", data)

    def failed(self, data):
        self.__send_notification("failed", data)

    def running(self, data):
        self.__send_notification("running", data)


