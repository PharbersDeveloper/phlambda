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
        paginator = self.dynamodb_client.get_paginator("query")

        response_iterator = paginator.paginate(
            TableName=table_name,
            KeyConditionExpression=expression["FilterExpression"],
            ExpressionAttributeNames=expression["ExpressionAttributeNames"],
            ExpressionAttributeValues=expression["ExpressionAttributeValues"],
            PaginationConfig={
                "MaxItems": limit,
                "PageSize": limit,
                "StartingToken": start_key
            }
        )
        result = response_iterator.build_full_result()
        return {
            "data": list(map(self.__dynamoData2EntityData, result.get("Items", []))),
            "start_key": result.get("NextToken", "")
        }

    def scanTable(self, data):
        table_name = data["table_name"]
        limit = data["limit"]
        expression = data["expression"]
        start_key = data["start_key"]
        paginator = self.dynamodb_client.get_paginator("scan")

        response_iterator = paginator.paginate(
            TableName=table_name,
            FilterExpression=expression["FilterExpression"],
            ExpressionAttributeNames=expression["ExpressionAttributeNames"],
            ExpressionAttributeValues=expression["ExpressionAttributeValues"],
            PaginationConfig={
                "MaxItems": limit,
                "PageSize": limit,
                "StartingToken": start_key
            }
        )
        result = response_iterator.build_full_result()
        return {
            "data": list(map(self.__dynamoData2EntityData, result.get("Items", []))),
        }
