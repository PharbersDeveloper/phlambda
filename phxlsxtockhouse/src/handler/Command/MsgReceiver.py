from handler.Command.Receiver import Receiver
import constants.Common as Common
import logging
import json
import time


class MsgReceiver(Receiver):

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]

    def __send_notification(self, status, message):
        logging.debug("Alex Notification ====> \n")
        self.dynamodb.putData({
            "table_name": "notification",
            "item": {
                "id": message["id"],
                "projectId": message["project_id"],
                "code": 0,
                "comments": "",
                "date": int(round(time.time() * 1000)),
                "jobCat": "notification",
                "jobDesc": status,
                "message": json.dumps({
                    "type": "operation",
                    "opname": message["owner"],
                    "opgroup": message.get("opgroup", "-1"),
                    "cnotification": {
                        "status": f"""{message["prefix"]}{status}""",
                        "data": json.dumps(message.get("data", {}), ensure_ascii=False),
                        "error": json.dumps(message.get("error", {}), ensure_ascii=False)
                    }
                }, ensure_ascii=False),
                "owner": message["owner"],
                "showName": message["showName"]
            }
        })

    def succeed(self, data):
        self.__send_notification("succeed", data)

    def failed(self, data):
        self.__send_notification("failed", data)

    def running(self, data):
        self.__send_notification("running", data)


