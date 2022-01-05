from handler.Command.Receiver import Receiver
import constants.Common as Common
import logging
import json
import time


class MsgReceiver(Receiver):

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]

    def __update_action(self, status, data):
        action_item = dict({}, **data["data"])
        action_item["message"] = json.dumps(action_item["message"], ensure_ascii=False)
        action_item["jobDesc"] = status
        action_item["date"] = int(round(time.time() * 1000))
        self.dynamodb.putData({
            "table_name": "action",
            "item": action_item
        })

    def __send_notification(self, status, data):
        action_item = data["data"]
        message = action_item["message"][0]
        logging.debug("Alex Notification ====> \n")
        self.dynamodb.putData({
            "table_name": "notification",
            "item": {
                "id": action_item["id"],
                "projectId": action_item["projectId"],
                "code": 0,
                "comments": "",
                "date": int(round(time.time() * 1000)),
                "jobCat": "notification",
                "jobDesc": status,
                "message": json.dumps({
                    "type": "operation",
                    "opname": action_item["owner"],
                    "opgroup": message.get("opgroup", "-1"),
                    "cnotification": {
                        "status": f"""{data["prefix"]}{status}""",
                        "data": json.dumps(message.get("data", {}), ensure_ascii=False),
                        "error": json.dumps(data.get("error", {}), ensure_ascii=False)
                    }
                }, ensure_ascii=False),
                "owner": action_item["owner"],
                "showName": action_item["showName"]
            }
        })

    def succeed(self, data):
        self.__update_action("succeed", data)
        self.__send_notification("succeed", data)

    def failed(self, data):
        self.__update_action("failed", data)
        self.__send_notification("failed", data)

