import json

import boto3
import util.AWS.define_value as dv
from boto3.dynamodb.conditions import Key, Attr


class DynamoDB(object):

    def __init__(self, **kwargs):
        self.access_key = kwargs.get("access_key", None)
        self.secret_key = kwargs.get("secret_key", None)
        if self.access_key and self.secret_key:
            self.dynamodb_resource = boto3.resource("dynamodb", region_name=dv.AWS_REGION,
                                                    aws_access_key_id=self.access_key,
                                                    aws_secret_access_key=self.secret_key)
            return
        self.sts = kwargs.get("sts", None)
        if self.sts and self.sts.credentials:
            self.dynamodb_resource = boto3.resource("dynamodb", **self.sts.get_cred())
            return
        self.dynamodb_resource = boto3.resource("dynamodb", region_name=dv.AWS_REGION)

    def queryTableWithPartitionKey(self, table, partition_key, partition_value):
        ds_table = self.dynamodb_resource.Table(table)
        res = ds_table.query(
            KeyConditionExpression=Key(partition_key).eq(partition_value)
        )
        return res

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

    def batch_write(self, table, data):
        self.dynamodb_resource.batch_write_item(
            RequestItems={
                table: data
            }
        )

    def delete_item(self, data):
        table_name = data.get("table_name")
        key = data.get("key")
        table = self.dynamodb_resource.Table(table_name)
        try:
            table.delete_item(
                Key=key,
            )
            return "删除成功"
        except Exception as e:
            return "删除失败:" + json.loads(str(e))
