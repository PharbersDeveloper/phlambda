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
        del AttributeUpdates["projectId"]
        del AttributeUpdates["id"]
        data = {
            "table_name": table_name,
            "Key": Key,
            "AttributeUpdates": AttributeUpdates
        }
        print(data)
        # self.dynamodb.updateData(data)

    def updateNotification(self, item, table_name, dag_conf, status=" "):
        message = {
            "type": "notification",
            "opname": item.get("owner"),
            "cnotification": {
                "jobId": dag_conf.get("jobId"),
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
        del AttributeUpdates["projectId"]
        del AttributeUpdates["id"]
        data = {
            "table_name": table_name,
            "Key": Key,
            "AttributeUpdates": AttributeUpdates
        }
        # self.dynamodb.updateData(data)

    def updata_targetId(self, item, table_name, jobId):
