import boto3
import constants.DefinValue as Common
from util.GenerateID import GenerateID


class DynamoDB:

    def __init__(self, **kwargs):
        self.edition = "_dev" if os.getenv("EDITION") == "DEV" else ""
        self.access_key = kwargs.get("access_key", None)
        self.secret_key = kwargs.get("secret_key", None)
        if self.access_key and self.secret_key:
            self.dynamodb_resource = boto3.resource("dynamodb", region_name=Common.AWS_REGION,
                                                    aws_access_key_id=self.access_key,
                                                    aws_secret_access_key=self.secret_key)
            return
        self.sts = kwargs.get("sts", None)
        if self.sts and self.sts.credentials:
            self.dynamodb_resource = boto3.resource("dynamodb", **self.sts.get_cred())
            return
        self.dynamodb_resource = boto3.resource("dynamodb", region_name=Common.AWS_REGION)

    def queryTable(self, data):
        table_name = data["table_name"] + self.edition
        limit = data["limit"]
        expression = data["expression"]
        start_key = data["start_key"]
        table = self.dynamodb_resource.Table(table_name)
        try:
            if len(start_key) == 0:
                result = table.query(
                    KeyConditionExpression=expression,
                    Limit=limit,
                )
            else:
                result = table.query(
                    KeyConditionExpression=expression,
                    Limit=limit,
                    ExclusiveStartKey=start_key
                )
            return {
                "data": result.get("Items"),
                "start_key": result.get("LastEvaluatedKey", "{}")
            }
        except Exception as e:
            print(e)
            return {
                "data": [],
                "start_key": {}
            }

    def scanTable(self, data):
        table_name = data["table_name"] + self.edition
        limit = data["limit"]
        expression = data["expression"]
        start_key = data["start_key"]
        table = self.dynamodb_resource.Table(table_name)
        try:
            if len(start_key) == 0:
                result = table.scan(
                    FilterExpression=expression,
                    Limit=limit,
                )
            else:
                result = table.scan(
                    FilterExpression=expression,
                    Limit=limit,
                    ExclusiveStartKey=start_key
                )
            return {
                "data": result.get("Items"),
                "start_key": result.get("LastEvaluatedKey", "{}")
            }
        except Exception as e:
            print(e)
            return {
                "data": [],
                "start_key": {}
            }

    def putData(self, data):
        table_name = data["table_name"] + self.edition
        item = data["item"]
        if "id" not in item.keys():
            item["id"] = GenerateID.generate()
        table = self.dynamodb_resource.Table(table_name)
        table.put_item(
            Item=item
        )
        return {
            "data": item
        }

    def deleteData(self, data):
        table_name = data["table_name"] + self.edition
        keys = data["conditions"]
        table = self.dynamodb_resource.Table(table_name)
        table.delete_item(
            Key=keys
        )
        return {
            "status": "complete"
        }
