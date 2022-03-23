import json
import time

from util.AWS.DynamoDB import DynamoDB
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL

class UpdateAction:

    def __init__(self, **kwargs):
        self.dynamodb = DynamoDB()
        self.logger = PhLogging().phLogger("update_dynamodb_action", LOG_DEBUG_LEVEL)

    def updateItem(self, item, table_name, status=" "):
        item.update({"jobDesc": status})
        Key = {
            "id": item.get("id"),
            "projectId": item.get("projectId")
        }

        AttributeUpdates={}
        for key, value in item.items():
            update = {
                key: {
                    "Value": value,
                    "Action": "PUT"
                }
            }
            AttributeUpdates.update(update)
        if AttributeUpdates.get("id"):
            del AttributeUpdates["id"]
        if AttributeUpdates.get("projectId"):
            del AttributeUpdates["projectId"]
        data = {
            "table_name": table_name,
            "Key": Key,
            "AttributeUpdates": AttributeUpdates
        }
        self.dynamodb.updateData(data)

    def updateNotification(self, action_item, table_name, dag_conf, status=" "):

        data = {
            "table_name": "notification"
        }
        item = {}
        job_status = "failed"
        if status == "dag insert success":
            job_status = "succeed"

        message = {
            "type": "notification",
            "opname": action_item.get("owner"),
            "cnotification": {
                "jobName": str(dag_conf.get("jobName")),
                "jobPath": str(dag_conf.get("job_path")),
                "jobShowName": str(dag_conf.get("jobShowName")),
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

        item.update({"id": action_item.get("id", "default_id")})
        item.update({"projectId": action_item.get("projectId")})
        item.update({"category": ""})
        item.update({"code": "0"})
        item.update({"comments": ""})
        item.update({"date": str(int(round(time.time() * 1000)))})
        item.update({"jobCat": "notification"})
        item.update({"jobDesc": action_item.get("jobDesc")})
        item.update({"message": json.dumps(message, ensure_ascii=False)})
        item.update({"owner": action_item.get("owner")})
        item.update({"showName": action_item.get("showName")})
        item.update({"status": job_status})
        data.update({"item": item})
        print(data)
        self.dynamodb.putData(data)
        self.logger.debug("notification 创建完成")


    def updateDagConf(self, item):


        Key = {
            "projectId": item.get("projectId"),
            "jobName": item.get("jobName")
        }

        AttributeUpdates={}
        for key, value in item.items():
            update = {
                key: {
                    "Value": value,
                    "Action": "PUT"
                }
            }
            AttributeUpdates.update(update)
        del AttributeUpdates["projectId"]
        del AttributeUpdates["jobName"]
        data = {
            "table_name": "dagconf",
            "Key": Key,
            "AttributeUpdates": AttributeUpdates
        }
        self.dynamodb.updateData(data)
