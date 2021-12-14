import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID

class UpdateAction:

    def __init__(self, **kwargs):
        self.dynamodb = DynamoDB()

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
        # self.dynamodb.updateData(data)

    def updateNotification(self, item, table_name, dag_conf, status=" "):
        message = {
            "type": "notification",
            "opname": item.get("owner"),
            "cnotification": {
                "jobName": str(dag_conf.get("jobName")),
                "jobPath": str(dag_conf.get("job_path")),
                "status": status,
                "error": ""
            }
        }
        item.update({"jobDesc": status})
        item.update({"message": json.dumps(message,  ensure_ascii=False)})
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
            "key": Key,
            "AttributeUpdates": AttributeUpdates
        }
        self.dynamodb.updateData(data)

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
