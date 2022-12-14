import boto3
from constants.Common import Common
from boto3.dynamodb.conditions import Attr


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

    def getTableCount(self, tableName, projectId):
        result = self.dynamodb_resource.Table(tableName)
        result = result.scan(
            Select='COUNT',
            FilterExpression=Attr("projectId").eq(projectId)
        )
        return result.get("Count", 0)

    def jupyterResourceCount(self):
        result = self.dynamodb_resource.Table("resource")
        result = result.scan(
            Select='COUNT',
            FilterExpression=Attr("ctype").eq("jupyter") | Attr("ctype").eq("jupyter")
        )
        return result.get("Count", 0)
