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
        "traceId.$": "ce1e04bfa52446c5ab2a1c8fe2b075b0",
        "projectId.$": "ggjpDje0HUC2JW",
        "owner.$": "test_owner",
        "showName.$": "$.test_showName",
        "projectName.$": "demo",
        "resources": {
            "projectName": "demo",
            "currentContext": "V2",
            "proxies": [
              "192.168.16.102"
            ],
            "dns": "https://ggjpDje0HUC2JW.pharbers.com/",
            "clusters": [
              {
                "type": "emr",
                "id": "j-1P7LCR5UW861G"
              }
            ],
            "olap": [
              {
                "type": "ch",
                "name": "proxy",
                "uri": "http://192.168.16.102:8123"
              },
              {
                "type": "ch",
                "name": "http",
                "uri": "http://192.168.16.102:8080/ch?"
              }
            ],
            "notification": "UjegmQ32Hn9ObUe",
            "commargs": [
              {
                "engine": "pyspark",
                "type": "spark-submit",
                "args": {
                  "spark.driver.cores": "1",
                  "spark.driver.memory": "2g",
                  "spark.executor.cores": "2",
                  "spark.executor.memory": "4g",
                  "spark.executor.instances": "2",
                  "spark.driver.extraJavaOptions": "-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8 -Dcom.amazonaws.services.s3.enableV4",
                  "spark.executor.extraJavaOptions": "-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8 -Dcom.amazonaws.services.s3.enableV4"
                }
              }
            ]
        },
        "result": {
            "datasets": [
                  {
                    "projectId": "ggjpDje0HUC2JW",
                    "path": "",
                    "schema": "[]",
                    "prop": "",
                    "sample": "F_1",
                    "label": "[]",
                    "name": "555a",
                    "date": "1652089651976",
                    "cat": "intermediate",
                    "id": "BIfNgEpTgK67H23",
                    "traceId": "7c0f3f273eeb47769729ede3554f1ba8",
                    "format": "parquet"
                  },
                  {
                    "projectId": "ggjpDje0HUC2JW",
                    "path": " ",
                    "schema": "[{\"src\":\"11111\",\"des\":\"11111\",\"type\":\"String\"},{\"src\":\"商品名称\",\"des\":\"商品名称\",\"type\":\"String\"},{\"src\":\"生产企业\",\"des\":\"生产企业\",\"type\":\"String\"},{\"src\":\"剂型\",\"des\":\"剂型\",\"type\":\"String\"},{\"src\":\"规格\",\"des\":\"规格\",\"type\":\"String\"},{\"src\":\"包装数量\",\"des\":\"包装数量\",\"type\":\"String\"},{\"src\":\"包装单位\",\"des\":\"包装单位\",\"type\":\"String\"},{\"src\":\"packcode\",\"des\":\"packcode\",\"type\":\"String\"},{\"src\":\"xiangmu\",\"des\":\"xiangmu\",\"type\":\"String\"},{\"src\":\"version\",\"des\":\"version\",\"type\":\"String\"}]",
                    "prop": " ",
                    "sample": "F_1",
                    "label": "[]",
                    "name": "444a",
                    "date": "1652089634363",
                    "cat": "intermediate",
                    "id": "6ZpR3CStp5pYTnp",
                    "traceId": "6ed0cff485e347df8bafa7a27f19cdb3",
                    "format": "parquet"
                  }
            ],
            "scripts": [
                  {
                    "projectId": "ggjpDje0HUC2JW",
                    "operatorParameters": "",
                    "actionName": "compute_555a",
                    "outputs": "555a",
                    "runtime": "prepare",
                    "showName": "张璐",
                    "jobDisplayName": "demo_demo_developer_compute_555a",
                    "jobVersion": "developer",
                    "prop": "",
                    "jobId": "js1jPtkSmpVCGpw",
                    "projectName": "demo",
                    "jobPath": "2020-11-11/jobs/python/phcli/demo_demo_developer/demo_demo_developer_compute_555a/phjob.py",
                    "jobName": "developer_js1jPtkSmpVCGpw_demo_demo_compute_555a",
                    "timeout": 1000,
                    "dagName": "demo",
                    "labels": "",
                    "jobShowName": "compute_555a",
                    "owner": "c89b8123-a120-498f-963c-5be102ee9082",
                    "flowVersion": "developer",
                    "id": "js1jPtkSmpVCGpw",
                    "traceId": "7c0f3f273eeb47769729ede3554f1ba8",
                    "inputs": "[\"Alex\"]"
                  },
                  {
                    "projectId": "ggjpDje0HUC2JW",
                    "operatorParameters": "",
                    "actionName": "compute_444a",
                    "outputs": "444a",
                    "runtime": "sparkr",
                    "showName": "张璐",
                    "jobDisplayName": "demo_demo_developer_compute_444a",
                    "jobVersion": "developer",
                    "prop": "",
                    "jobId": "zwiPnNzmz0oir5w",
                    "projectName": "demo",
                    "jobPath": "2020-11-11/jobs/python/phcli/demo_demo_developer/demo_demo_developer_compute_444a/phjob.R",
                    "jobName": "developer_zwiPnNzmz0oir5w_demo_demo_compute_444a",
                    "timeout": 1000,
                    "dagName": "demo",
                    "labels": "",
                    "jobShowName": "compute_444a",
                    "owner": "c89b8123-a120-498f-963c-5be102ee9082",
                    "flowVersion": "developer",
                    "id": "zwiPnNzmz0oir5w",
                    "traceId": "6ed0cff485e347df8bafa7a27f19cdb3",
                    "inputs": "[\"Alex\"]"
                  },
                  {
                    "projectId": "ggjpDje0HUC2JW",
                    "operatorParameters": "",
                    "actionName": "compute_444a",
                    "outputs": "444a",
                    "runtime": "sparkr",
                    "showName": "张璐",
                    "jobDisplayName": "demo_demo_developer_compute_444a",
                    "jobVersion": "developer",
                    "prop": "",
                    "jobId": "zwiPnNzmz0oir5w",
                    "projectName": "demo",
                    "jobPath": "2020-11-11/jobs/python/phcli/demo_demo_developer/demo_demo_developer_compute_444a/phjob.R",
                    "jobName": "developer_zwiPnNzmz0oir5w_demo_demo_compute_444a",
                    "timeout": 1000,
                    "dagName": "demo",
                    "labels": "",
                    "jobShowName": "compute_444a",
                    "owner": "c89b8123-a120-498f-963c-5be102ee9082",
                    "flowVersion": "developer",
                    "id": "zwiPnNzmz0oir5w",
                    "traceId": "6ed0cff485e347df8bafa7a27f19cdb3",
                    "inputs": "[\"Alex\"]"
                  }
            ],
            "links": [
                  {
                    "projectId": "ggjpDje0HUC2JW",
                    "ctype": "node",
                    "runtime": "prepare",
                    "prop": "",
                    "cmessage": "compute_555a",
                    "sortVersion": "developer_js1jPtkSmpVCGpw",
                    "representId": "js1jPtkSmpVCGpw",
                    "name": "compute_555a",
                    "cat": "job",
                    "level": "",
                    "flowVersion": "developer",
                    "position": "",
                    "traceId": "7c0f3f273eeb47769729ede3554f1ba8"
                  },
                  {
                    "projectId": "ggjpDje0HUC2JW",
                    "ctype": "link",
                    "runtime": "",
                    "prop": "",
                    "cmessage": "{\"sourceId\": \"js1jPtkSmpVCGpw\", \"sourceName\": \"compute_555a\", \"targetId\": \"BIfNgEpTgK67H23\", \"targetName\": \"555a\"}",
                    "sortVersion": "developer_kJMsxLoYGBfbuEC",
                    "representId": "kJMsxLoYGBfbuEC",
                    "name": "empty",
                    "cat": "",
                    "level": "",
                    "flowVersion": "developer",
                    "position": "",
                    "traceId": "7c0f3f273eeb47769729ede3554f1ba8"
                  },
                  {
                    "projectId": "ggjpDje0HUC2JW",
                    "ctype": "link",
                    "runtime": "",
                    "prop": "",
                    "cmessage": "{\"sourceId\": \"f1801eb22d79cbd6325d23ca74fc954e.xlsx\", \"sourceName\": \"Alex\", \"targetId\": \"js1jPtkSmpVCGpw\", \"targetName\": \"compute_555a\"}",
                    "sortVersion": "developer_8Q8fERHQToKO9iF",
                    "representId": "8Q8fERHQToKO9iF",
                    "name": "empty",
                    "cat": "",
                    "level": "",
                    "flowVersion": "developer",
                    "position": "",
                    "traceId": "7c0f3f273eeb47769729ede3554f1ba8"
                  },
                  {
                    "projectId": "ggjpDje0HUC2JW",
                    "ctype": "node",
                    "runtime": "sparkr",
                    "prop": "",
                    "cmessage": "compute_444a",
                    "sortVersion": "developer_zwiPnNzmz0oir5w",
                    "representId": "zwiPnNzmz0oir5w",
                    "name": "compute_444a",
                    "cat": "job",
                    "level": "",
                    "flowVersion": "developer",
                    "position": "",
                    "traceId": "6ed0cff485e347df8bafa7a27f19cdb3"
                  },
                  {
                    "projectId": "ggjpDje0HUC2JW",
                    "ctype": "link",
                    "runtime": "",
                    "prop": "",
                    "cmessage": "{\"sourceId\": \"zwiPnNzmz0oir5w\", \"sourceName\": \"compute_444a\", \"targetId\": \"6ZpR3CStp5pYTnp\", \"targetName\": \"444a\"}",
                    "sortVersion": "developer_AWEtrP36T9drIzZ",
                    "representId": "AWEtrP36T9drIzZ",
                    "name": "empty",
                    "cat": "",
                    "level": "",
                    "flowVersion": "developer",
                    "position": "",
                    "traceId": "6ed0cff485e347df8bafa7a27f19cdb3"
                  },
                  {
                    "projectId": "ggjpDje0HUC2JW",
                    "ctype": "link",
                    "runtime": "",
                    "prop": "",
                    "cmessage": "{\"sourceId\": \"f1801eb22d79cbd6325d23ca74fc954e.xlsx\", \"sourceName\": \"Alex\", \"targetId\": \"zwiPnNzmz0oir5w\", \"targetName\": \"compute_444a\"}",
                    "sortVersion": "developer_I2uMcWcJAUCC3Wt",
                    "representId": "I2uMcWcJAUCC3Wt",
                    "name": "empty",
                    "cat": "",
                    "level": "",
                    "flowVersion": "developer",
                    "position": "",
                    "traceId": "6ed0cff485e347df8bafa7a27f19cdb3"
                  },
                  {
                    "projectId": "ggjpDje0HUC2JW",
                    "ctype": "node",
                    "runtime": "intermediate",
                    "prop": "{\"path\": \"\", \"partitions\": 1}",
                    "cmessage": "",
                    "sortVersion": "developer_BIfNgEpTgK67H23",
                    "representId": "BIfNgEpTgK67H23",
                    "name": "555a",
                    "cat": "dataset",
                    "level": "",
                    "flowVersion": "developer",
                    "position": "",
                    "traceId": "baf78a55809944b7838edfbb45a4f2b2"
                  },
                  {
                    "projectId": "ggjpDje0HUC2JW",
                    "ctype": "node",
                    "runtime": "intermediate",
                    "prop": "{\"path\": \"\", \"partitions\": 1}",
                    "cmessage": "",
                    "sortVersion": "developer_6ZpR3CStp5pYTnp",
                    "representId": "6ZpR3CStp5pYTnp",
                    "name": "444a",
                    "cat": "dataset",
                    "level": "",
                    "flowVersion": "developer",
                    "position": "",
                    "traceId": "baf78a55809944b7838edfbb45a4f2b2"
                  }
            ]
        }
    }
'''


class CleanUp:
    name_list = []
    del_list = []
    dynamodb = boto3.resource("dynamodb", region_name="cn-northwest-1",
                              aws_access_key_id="AKIAWPBDTVEANKEW2XNC",
                              aws_secret_access_key="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")

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
