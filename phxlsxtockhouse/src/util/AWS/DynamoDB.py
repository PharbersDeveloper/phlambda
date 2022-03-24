import boto3
import constants.DefinValue as Common
from util.GenerateID import GenerateID
from util.ClieckHouse import SingletonMetaClass


class DynamoDB(metaclass=SingletonMetaClass):

    def __init__(self, **kwargs):
        self.access_key = kwargs.get("access_key", None)
        self.secret_key = kwargs.get("secret_key", None)
        if self.access_key and self.secret_key:
            self.dynamodb_resource = boto3.resource("dynamodb", region_name=Common.AWS_REGION,
                                                    aws_access_key_id=self.access_key,
                                                    aws_secret_access_key=self.secret_key)
            self.dynamodb_client = boto3.client("dynamodb", region_name=Common.AWS_REGION,
                                                aws_access_key_id=self.access_key,
                                                aws_secret_access_key=self.secret_key)
            return
        self.sts = kwargs.get("sts", None)
        if self.sts and self.sts.credentials:
            self.dynamodb_resource = boto3.resource("dynamodb", **self.sts.get_cred())
            self.dynamodb_client = boto3.client("dynamodb", **self.sts.get_cred())
            return
        self.dynamodb_resource = boto3.resource("dynamodb", region_name=Common.AWS_REGION)
        self.dynamodb_client = boto3.client("dynamodb", region_name=Common.AWS_REGION)

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
        if len(item.get("id", "")) == 0:
            del item["id"]
        table = self.dynamodb_resource.Table(table_name)
        table.put_item(
            Item=item
        )
        return {
            "data": item
        }

    def deleteData(self, data):
        table_name = data["table_name"]
        keys = data["conditions"]
        table = self.dynamodb_resource.Table(table_name)
        table.delete_item(
            Key=keys
        )
        return {
            "status": "complete"
        }

    def __dynamoData2EntityData(self, record):
        item = {}
        for field in list(record.keys()):
            value = record[field]
            v_k = list(value.keys())[0]
            item[field] = value[v_k]
        return item

    def batchGetItem(self, data):
        table_name = data["table_name"]
        expression = data["expression"]
        result = self.dynamodb_client.batch_get_item(
            RequestItems={
                f"{table_name}": {
                    "Keys": expression
                }
            }
        )
        items = result["Responses"].get(table_name, [])
        data = list(map(self.__dynamoData2EntityData, items))
        return {
            "data": data,
            "start_key": {}
        }
