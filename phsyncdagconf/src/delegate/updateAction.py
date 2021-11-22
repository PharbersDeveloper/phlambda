import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID

class UpdateAction:

    def __init__(self, **kwargs):
        self.dynamodb = DynamoDB()

    def updateItem(self, item_list, status="dag_conf insert success"):
        for item in item_list:
            print(item)
            item.update({"jobCat": status})
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
                "table_name": "action",
                "Key": Key,
                "AttributeUpdates": AttributeUpdates
            }
            print(data)
            self.dynamodb.updateData(data)
        pass