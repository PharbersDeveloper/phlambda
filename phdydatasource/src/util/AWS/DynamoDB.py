import boto3
from constants.Common import Common
# import base64
# from boto3.dynamodb.conditions import Key, Attr
# from src.util.AWS.STS import STS


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

    def queryTable(self, table_name, limit, expression, start_key):
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

    def scanTable(self, table_name, limit, expression, start_key):
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


# if __name__ == '__main__':
#     sts = STS().assume_role(
#         base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
#         "Ph-Back-RW"
#     )
#
#     dynamodb = DynamoDB(sts=sts)
#     result = dynamodb.queryTable("step", 1000000, Key("id").eq("22D3MKI2A4NUjG0"), "")
#     print(result)
