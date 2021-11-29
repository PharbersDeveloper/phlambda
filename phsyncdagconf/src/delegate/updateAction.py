import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID

class UpdateAction:

    def __init__(self, **kwargs):
        self.dynamodb = DynamoDB()

    def updateItem(self, item_list, table_name, status=" "):
        for item in item_list:
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
            self.dynamodb.updateData(data)

    def update_notification(self, item_list, table_name, status=" "):
        message = {
            "type": "notification",
            "opname": "c89b8123-a120-498f-963c-5be102ee9082",
            "opgroup": "zudIcG_17yj8CEUoCTHg",
            "cnotification": {
                "status": "upload_succeed",
                "error": ""
            }
        }
        pass