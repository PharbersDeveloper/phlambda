import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID

class UpdateAction:

    def __init__(self, **kwargs):
        self.dynamodb = DynamoDB()

    def updateItem(self, item_list, table_name, status="dag_conf insert success"):
        for item in item_list:
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
                "table_name": table_name,
                "Key": Key,
                "AttributeUpdates": AttributeUpdates
            }
            # self.dynamodb.updateData(data)