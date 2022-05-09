import json
import boto3
from boto3.dynamodb.conditions import Attr, Key

'''
这个函数实现两件事情：
1. 将错误的信息写入 notification 中
2. 将错误的被删除的 index 重新写回 dynamodb 中
    所有的信息都在 result 中存放

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "projectName.$": "$.common.projectName",
        "resources": {
    
        },
        "result": {
            "datasets": [{
                "id": "",
                ...
            }],
            "script": {
                "id": "",
                ...
            },
            "links": [{
                "id": "",
                ...
            }]
        }
    }
'''


class CleanUp:
    name_list = []
    del_list = []
    dynamodb = boto3.resource("dynamodb", region_name="cn-northwest-1",
                               aws_access_key_id="AKIAWPBDTVEANKEW2XNC",
                               aws_secret_access_key="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")

    def query_dataset(self, name):
        table = self.dynamodb.Table("dataset")
        response = table.query(
            IndexName='dataset-projectId-name-index',
            KeyConditionExpression=Key('projectId').eq(self.projectId) & Key("name").eq(name),
        )
        return response.get("Items")

    def query_dag(self):
        table = self.dynamodb.Table("dag")
        response = table.query(
            KeyConditionExpression=Key('projectId').eq(self.projectId),
        )
        return response.get("Items")

    def put_item(self, table_name):
        item = {

        }
        table = self.dynamodb.Table(table_name)
        response = table.put_item(
            Item=item
        )

    def update_item(self, table_name, col_name, col_value, value):
        table = self.dynamodb.Table(table_name)
        table.update_item(
            Key={
                col_name: col_value,
                "projectId": self.projectId
            },
            UpdateExpression="SET cat = :str",
            ExpressionAttributeValues={
                ":str": f"{value}"
            }
        )

    def run(self, projectId, datasets, scripts, traceId, **kwargs):

        self.projectId = projectId
        self.name_list.append(scripts.get("actionName"))


def lambda_handler(event, context):
    CleanUp().run(**event)
    return True
