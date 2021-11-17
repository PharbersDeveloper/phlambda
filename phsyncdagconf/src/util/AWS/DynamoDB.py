import boto3
from constants.Common import Common
from util.GenerateID import GenerateID


class DynamoDB:

    def __init__(self, **kwargs):
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
        table_name = data["table_name"]
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
        table_name = data["table_name"]
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
        table_name = data["table_name"]
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

    def updateData(self, data):
        table = self.dynamodb_resource.Table("dag")
        partition_key = data["partition_key"]
        sort_key = data["sort_key"]
        key = {}
        key.update(partition_key)
        key.update(sort_key)
        table.update_item(
            Key={
                "projectId": "123",
                "representId": "321"
            },
            AttributeUpdates={
                "cat": {
                    "Value": "2",
                    "Action": "PUT"
                },
                "cmessage": {
                    "Value": "messsssss",
                    "Action": "PUT"
                },
                "ctyoe": {
                    "Value": "node",
                    "Action": "PUT"
                }

            }
        )

