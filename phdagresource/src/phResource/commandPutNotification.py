import time
import json
from phResource.command import Command
from util.AWS.DynamoDB import DynamoDB
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL
from util.GenerateID import GenerateID


class CommandPutNotification(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.dynamodb = DynamoDB()

    def execute(self):
        # 创建 target group
        # 192.168.16.119
        logger = PhLogging().phLogger("put_notification", LOG_DEBUG_LEVEL)
        logger.debug("notification 创建流程")
        data = {
            "table_name": "notification"
        }
        item = {}
        status = "resource create success"
        message = {
            "type": "notification",
            "opname": self.project_message.get("owner"),
            "cnotification": {
                "status": status,
                "error": json.dumps({
                    "code": "123",
                    "message": {
                        "zh": status,
                        "en": status
                    }
                }, ensure_ascii=False)
            }
        }

        item.update({"id": self.action_id})
        item.update({"projectId": self.project_message.get("projectId")})
        item.update({"category": ""})
        item.update({"code": "0"})
        item.update({"commnets": ""})
        item.update({"date": str(int(round(time.time() * 1000)))})
        item.update({"jobCat": "notification"})
        item.update({"jobDesc": self.operate_type})
        item.update({"message": json.dumps(message, ensure_ascii=False)})
        item.update({"owner": self.project_message.get("owner")})
        item.update({"showName": self.project_message.get("showName")})
        item.update({"status": "succeed"})
        data.update({"item": item})
        print(data)
        self.dynamodb.putData(data)
        logger.debug("notification 创建完成")
