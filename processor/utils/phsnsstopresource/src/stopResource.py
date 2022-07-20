import boto3
import uuid
from boto3.dynamodb.conditions import Key, Attr
from abc import ABC, abstractmethod


class StopResource(ABC):

    def query_resource(self, tenantId, ctype):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('resource')
        res = table.query(
            KeyConditionExpression=Key("tenantId").eq(tenantId),
            FilterExpression=Attr("ctype").eq(ctype)
        )

        return res["Items"]

    @property
    def get_uuid(self):
        uu_id = uuid.uuid4()
        suu_id = ''.join(str(uu_id).split('-'))
        return suu_id

    @abstractmethod
    def run(self, tenantId, ctype):
        pass
