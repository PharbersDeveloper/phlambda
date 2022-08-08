import boto3
from constants.Common import Common
from util.GenerateID import GenerateID
from functools import reduce


class DynamoDB:

    def __init__(self, **kwargs):
        self.access_key = kwargs.get("access_key", None)
        self.secret_key = kwargs.get("secret_key", None)
        if self.access_key and self.secret_key:
            self.dynamodb_client = boto3.client("dynamodb", region_name=Common.AWS_REGION,
                                                aws_access_key_id=self.access_key,
                                                aws_secret_access_key=self.secret_key)
            return
        self.sts = kwargs.get("sts", None)
        if self.sts and self.sts.credentials:
            self.dynamodb_client = boto3.client("dynamodb", **self.sts.get_cred())
            return
        self.dynamodb_client = boto3.client("dynamodb", region_name=Common.AWS_REGION)

    def __dynamoData2EntityData(self, record):
        item = {}
        for field in list(record.keys()):
            value = record[field]
            v_k = list(value.keys())[0]
            item[field] = value[v_k]
        return item

    def queryTable(self, data):
        table_name = data["table_name"]
        limit = data["limit"]
        expression = data["expression"]
        start_key = data["start_key"]
        index_name = data["index_name"]
        paginator = self.dynamodb_client.get_paginator("query")

        parameter = {
            "TableName": table_name,
            "ScanIndexForward": False,
            "KeyConditionExpression": expression["FilterExpression"],
            "ExpressionAttributeNames": expression["ExpressionAttributeNames"],
            "ExpressionAttributeValues": expression["ExpressionAttributeValues"],
            "PaginationConfig": {
                "MaxItems": limit,
                "PageSize": limit,
                "StartingToken": start_key
            }
        }

        count_parameter = {
            "TableName": table_name,
            "Select": "COUNT",
            "ScanIndexForward": False,
            "KeyConditionExpression": expression["FilterExpression"],
            "ExpressionAttributeNames": expression["ExpressionAttributeNames"],
            "ExpressionAttributeValues": expression["ExpressionAttributeValues"],
        }

        if index_name is not None:
            parameter.update({"IndexName": index_name})
            count_parameter.update({"IndexName": index_name})

        try:
            count_result = self.dynamodb_client.query(**count_parameter)
            response_iterator = paginator.paginate(**parameter)
            result = response_iterator.build_full_result()
            return {
                "data": list(map(self.__dynamoData2EntityData, result.get("Items", []))),
                "start_key": result.get("NextToken", ""),
                "pre_key": start_key if start_key else "",
                "total_count": count_result["Count"]
            }
        except Exception as e:
            print(e)
            return {
                "data": [],
                "start_key": "",
                "pre_key": "",
                "total_count": 0
            }

    def scanTable(self, data):
        table_name = data["table_name"]
        limit = data["limit"]
        expression = data["expression"]
        start_key = data["start_key"]
        paginator = self.dynamodb_client.get_paginator("scan")

        parameter = {
            "TableName": table_name,
            "FilterExpression": expression["FilterExpression"],
            "ExpressionAttributeNames": expression["ExpressionAttributeNames"],
            "ExpressionAttributeValues": expression["ExpressionAttributeValues"],
            "PaginationConfig": {
                "MaxItems": limit,
                "PageSize": limit,
                "StartingToken": start_key
            }
        }

        count_parameter = {
            "TableName": table_name,
            "Select": "COUNT",
            "FilterExpression": expression["FilterExpression"],
            "ExpressionAttributeNames": expression["ExpressionAttributeNames"],
            "ExpressionAttributeValues": expression["ExpressionAttributeValues"],
        }

        try:
            count_result = self.dynamodb_client.query(**count_parameter)
            response_iterator = paginator.paginate(**parameter)
            result = response_iterator.build_full_result()
            return {
                "data": list(map(self.__dynamoData2EntityData, result.get("Items", []))),
                "start_key": result.get("NextToken", ""),
                "pre_key": start_key if start_key else "",
                "total_count": count_result["Count"]
            }
        except Exception as e:
            print(e)
            return {
                "data": [],
                "start_key": "",
                "pre_key": "",
                "total_count": 0
            }

    def putData(self, data):
        table_name = data["table_name"]
        item = data["item"]
        if "id" not in item.keys():
            item["id"] = GenerateID.generate()

        __dynamodb_type = {
            "str": "S",
            "int": "N",
            "float": "N",
            "bool": "BOOL"
        }

        def get_type(target):
            return str(type(target)).replace("<class", "").replace("'", "").replace(">", "").replace(" ", "")

        def join_data(key):
            value_type = get_type(item[key])
            value = item[key]
            if value_type != "bool":
                value = str(value)
            return {key: {__dynamodb_type[value_type]: value}}

        self.dynamodb_client.put_item(
            TableName=table_name,
            Item=reduce(lambda p, n: {**p, **n}, list(map(join_data, item.keys())))
        )
        return {
            "data": item
        }

    def deleteData(self, data):
        table_name = data["table_name"]
        keys = data["conditions"]
        self.dynamodb_client.delete_item(
            TableName=table_name,
            Key=reduce(lambda p, n: {**p, **n}, list(map(lambda x: {x: {"S": str(keys[x])}}, keys.keys())))
        )
        return {
            "status": "complete"
        }

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
            "data": data
        }
