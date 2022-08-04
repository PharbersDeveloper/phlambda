import time
import boto3
import json
from pherrorlayer import *


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
    dynamodb = boto3.resource("dynamodb", region_name="cn-northwest-1")

    def put_item(self, table_name, item):
        table = self.dynamodb.Table(table_name)
        response = table.put_item(
            Item=item
        )

    def run(self, datasets, scripts, links, **kwargs):
        for dataset in datasets:
            self.put_item("dataset", dataset)
        for script in scripts:
            self.put_item("dagconf", script)
        for link in links:
            self.put_item("dag", link)


def errors_adapter(error):
    error = json.loads(error)
    Command = {
        "datasets or scripts Missing field": ParameterError,
        "scripts type error": ParameterError,
        "datasets type error": ParameterError,
        "datasets name already exits": ParameterError,
        "dagconf actionName already exits": ParameterError,
        "common not exits": ParameterError,
        "action_not_exits": ParameterError,
        "notificaiton not exits": ParameterError,
        "datasets scripts not exits": ParameterError
    }
    errorMessage = error.get("errorMessage").replace(" ", "_")
    return serialization(Command[errorMessage])


def lambda_handler(event, context):
    result = event.get("result")
    errors = event.get("errors")
    CleanUp().run(**result)
    # 1. 将错误的信息写入 notification 中
    # 2. 将错误的被删除的 index 重新写回 dynamodb 中
    #     所有的信息都在 result 中存放
    return {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": errors_adapter(errors.get("Cause"))
        }
    }
