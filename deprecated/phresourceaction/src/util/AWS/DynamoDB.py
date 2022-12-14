import json

import boto3
from constants.Common import Common
from util.GenerateID import GenerateID
from util.AWS.STS import STS
from boto3.dynamodb.conditions import Key, Attr

class DynamoDB(object):

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
        table_name = data.get("table_name")
        partition_key = data["partition_key"]
        partition_value = data["partition_value"]
        ds_table = self.dynamodb_resource.Table(table_name)
        res = ds_table.query(
            # AttributesToGet=[
            #     "level"
            # ],
            KeyConditionExpression=Key(partition_key).eq(partition_value)
        )
        return res

    def queryTableBeginWith(self, data):
        table_name = data.get("table_name")
        partition_key = data["partition_key"]
        partition_value = data["partition_value"]
        sort_key = data["sort_key"]
        sort_value = data["sort_value"]
        ds_table = self.dynamodb_resource.Table(table_name)
        res = ds_table.query(
            # AttributesToGet=[
            #     "level"
            # ],
            KeyConditionExpression=Key(partition_key).eq(partition_value) & Key(sort_key).begins_with(sort_value)
        )
        return res

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
            return {
                "data": [],
                "start_key": {}
            }

    def putData(self, data):
        table_name = data["table_name"]
        item = data["item"]
        table = self.dynamodb_resource.Table(table_name)
        table.put_item(
            Item=item
        )
        return {
            "data": item
        }

    def updateData(self, data):
        table_name = data.get("table_name")
        key = data.get("key")
        attributeUpdates = data.get("AttributeUpdates")
        table = self.dynamodb_resource.Table(table_name)
        res = table.update_item(
            Key=key,
            AttributeUpdates=attributeUpdates
        )

    def getItem(self, data):
        table_name = data.get("table_name")
        key = data.get("key")
        table = self.dynamodb_resource.Table(table_name)
        res = table.get_item(
            Key=key,
            # AttributeToGet=[
            #     "level",
            #     "ctype"
            # ]
        )

        return res

    def query_attribute(self, data):
        table_name= data.get("table_name")
        attribute_key = data["attribute"].get("key")
        attribute_value = data["attribute"].get("value")
        table = self.dynamodb_resource.Table(table_name)
        res = table.scan(
            FilterExpression=Attr(attribute_key).eq(attribute_value),
        )
        return res

    def delete_item(self, data):
        table_name = data.get("table_name")
        key = data.get("key")
        table = self.dynamodb_resource.Table(table_name)
        try:
            res = table.delete_item(
                Key=key,
                # ReturnValues="ALL_OLD",
                # ConditionExpression=Attr(condition_key).begins_with(condition_value)
            )
            return "????????????"
        except Exception as e:
            return "????????????:" + json.loads(str(e))

    def delete_dag_conf_item_by_partitionkey_sortkey(self, query_data, delete_data):
        # ?????????query ?????????query????????????
        res = self.queryTableBeginWith(query_data)
        delete_partitionKey = delete_data.get("partitionKey")
        delete_sortKey = delete_data.get("sortKey")
        for item in res.get("Items"):

            key = {
                delete_partitionKey: item.get(delete_partitionKey),
                delete_sortKey: item.get(delete_sortKey),
            }
            data = {
                "table_name": delete_data.get("table_name"),
                "key": key
            }
            self.delete_item(data)

    def delete_dag_item_by_partitionkey_sortkey(self, query_data, delete_data, dag_conf_outputs):
        # ?????????query ?????????query????????????
        res = self.queryTableBeginWith(query_data)
        delete_partitionKey = delete_data.get("partitionKey")
        delete_sortKey = delete_data.get("sortKey")
        for item in res.get("Items"):
            if item.get("representId") not in dag_conf_outputs and item.get("cat") == "dataset":
                print("???????????????")
            else:
                key = {
                    delete_partitionKey: item.get(delete_partitionKey),
                    delete_sortKey: item.get(delete_sortKey),
                }
                data = {
                    "table_name": delete_data.get("table_name"),
                    "key": key
                }
                self.delete_item(data)

if __name__ == '__main__':
    auth = STS()
    sts = auth.assume_role(Common.ASSUME_ROLE_ARN, Common.ASSUME_ROLE_ARN)
    dy = DynamoDB(sts=sts)
    dy.updateData()