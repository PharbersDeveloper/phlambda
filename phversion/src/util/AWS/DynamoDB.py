import boto3
import os
from constants.Common import Common


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
        expression = data["expression"]
        start_key = data.get("start_key", '')
        table = self.dynamodb_resource.Table(table_name)
        # try:
        if len(start_key) == 0:
            result = table.query(
                KeyConditionExpression=expression,
            )
        else:
            result = table.query(
                KeyConditionExpression=expression,
                ExclusiveStartKey=start_key
            )
        return result.get("Items")
        #
        # except Exception as e:
        #     print(e)
        #     return []

    def scanTable(self, data):
        table_name = data["table_name"] + self.edition
        expression = data["expression"]
        start_key = data.get("start_key", '')
        table = self.dynamodb_resource.Table(table_name)
        try:
            if len(start_key) == 0:
                result = table.scan(
                    FilterExpression=expression,
                )
            else:
                result = table.scan(
                    FilterExpression=expression,
                    ExclusiveStartKey=start_key
                )
            return result.get("Items")

        except Exception as e:
            print(e)
            return []

    def putData(self, data):
        table_name = data["table_name"] + self.edition
        item = data["item"]
        # if "id" not in item.keys():
        #     item["id"] = GenerateID.generate()
        table = self.dynamodb_resource.Table(table_name)
        table.put_item(
            Item=item
        )
        return {
            "data": item
        }
