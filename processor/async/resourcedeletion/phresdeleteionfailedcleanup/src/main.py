import json
import time
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
            "datasets": [
                {
                    "name": "test_name",
                    "cat": "intermediate",
                    "format": "parquet"
                }
            ],
            "script": {
                "id": "String",
                "jobName": "String",
                "actionName": "String",
                "flowVersion": "developer",
                "inputs": "[]",
                "output": "{}"
            },
            "links": [{
                "id": "",
                ...
            }]，
            "errors": {
                "Error": "Exception",
                "Cause": ""
                }
        }
    }
'''


class CleanUp:
    name_list = []
    del_list = []
    dynamodb = boto3.resource("dynamodb", region_name="cn-northwest-1")

    def __init__(self, traceId, projectId, owner, showName, projectName, result, dagmsg, **kwargs):
        self.dagmsg = dagmsg
        self.traceId = traceId
        self.projectId = projectId
        self.owner = owner
        self.showName = showName
        self.projectName = projectName
        self.dsmsg = result.get("datasets")
        self.dagconfmsg = result.get("script")
        self.errors = result.get("errors")

    @property
    def dataset(self):
        return {
            "id": self.dsmsg.get("id"),
            "projectId": self.projectId,
            "date": int(time.time()),
            "label": self.dsmsg.get("label"),
            "name": self.dsmsg.get("name"),
            "schema": self.dsmsg.get("schema"),
            "version": self.dsmsg.get("version"),
            "cat": self.dsmsg.get("cat"),
            "path": self.dsmsg.get("path"),
            "format": self.dsmsg.get("format"),
            "prop": self.dsmsg.get("prop")
        }

    @property
    def dag(self):
        return {
            "projectId": self.projectId,
            "sortVersion": self.dagmsg.get("sortVersion"),
            "ctype": "node",
            "cat": "dataset",
            "level": "-99999",
            "runtime": self.dagmsg.get("runtime"),
            "cmessage": "",
            "flowVersion": self.dagmsg.get("flowVersion"),
            "name": self.dagmsg.get("name"),
            "position": '{"x": "0", "y": "0", "z": "0", "w": "0", "h": "0"}',
            "prop": self.dagmsg.get("prop"),
            "representId": self.dagmsg.get("prop")
        }

    @property
    def dagconf(self):
        return {
            "projectId": self.projectId,
            "jobName": self.dagconfmsg.get("jobName"),
            "traceId": self.traceId,
            "actionName": self.dagconfmsg.get("actionName"),
            "dagName": self.dagconfmsg.get("dagName"),
            "flowVersion": self.dagconfmsg.get("flowVersion"),
            "id": self.dagconfmsg.get("id"),
            "inputs": self.dagconfmsg.get("inputs"),
            "jobDisplayName": "developer",
            "jobId": self.dagconfmsg.get("jobId"),
            "jobPath": self.dagconfmsg.get("jobPath"),
            "jobShowName": self.dagconfmsg.get("jobShowName"),
            "jobVersion": self.dagconfmsg.get("jobVersion"),
            "labels": self.dagconfmsg.get("labels"),
            "operatorParameters": self.dagconfmsg.get("operatorParameters"),
            "outputs": self.dagconfmsg.get("outputs"),
            "owner": self.dagconfmsg.get("owner"),
            "projectName": self.dagconfmsg.get("projectName"),
            "prop": self.dagconfmsg.get("prop"),
            "runtime": self.dagconfmsg.get("runtime"),
            "showName": self.dagconfmsg.get("showName"),
            "targetJobId": self.dagconfmsg.get("targetJobId"),
            "timeout": 1000,
        }

    @property
    def notif_message(self):
        return {"type": "operation",
                "opname": "",
                "opgroup": "",
                "cnotification": {"data": "{}", "error": self.errors}}

    # @property
    # def notification(self):
    #     return {
    #         "id": self.data.get("id"),
    #         "projectId": self.data.get("projectId"),
    #         "category": self.data.get("category"),
    #         "code": self.data.get("code"),
    #         "comments": self.data.get("comments"),
    #         "date": int(time.time()*1000),
    #         "jobCat": "notification",
    #         "jobDesc": self.data.get("jobDesc"),
    #         "message": json.dumps(self.notif_message),
    #         "owner": self.data.get("owner"),
    #         "showName": self.data.get("showName"),
    #         "status": "succeed",
    #     }

    def query_item(self, table, index, traceId):
        table = self.dynamodb.Table(table)
        response = table.query(
            IndexName=index,
            KeyConditionExpression=Key('projectId').eq(self.projectId) & Key("traceId").eq(traceId),
        )
        return response.get("Items")

    def put_item(self, table_name, item):
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

    def run(self, **kwargs):
        self.update_item("notification", "id", "", self.notif_message)
        self.put_item("dataset", self.dataset)
        self.put_item("dag", self.dag)
        self.put_item("dagconf", self.dagconf)


def lambda_handler(event, context):
    CleanUp(**event).run()
    # 1. 将错误的信息写入 notification 中
    # 2. 将错误的被删除的 index 重新写回 dynamodb 中
    #     所有的信息都在 result 中存放
    return True
