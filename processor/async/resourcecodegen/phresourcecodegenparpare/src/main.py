import os
import yaml
from util.AWS.ph_s3 import PhS3
from upload2s3 import *
from phjob import *

'''
这个函数只做一件事情，在现有pyspark的脚本上重新创建。记住每次都是重新创建，基于steps的全image
********** 是镜像流程，不是插入删除流程 *********
args:
    event = { 
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "flowVersion": "developer",
        "dagName": "demo",
        "owner": "hbzhao",
        "showName": "赵浩博",
        "script": {
            "id": "",
            "jobName": "",
            "jobPath": "",
            "inputs": [],           // 现在没用，可能以后有用
            "outputs": [],          // 现在没用，可能以后有用
            "runtime": "prepare"
        },
        "steps": [                  // 这个地方特别需要注意，直接传最后需要保存的样子，（跳出删除修改插入的思想死循环）
            {
                "id": "alextest_demo_demo_developer_compute_十多个",
                "stepId": "1",
                "index": "1",
                "runtime": "prepare",
                "stepName": "Initial Filter On Value",
                "ctype": "FillEmptyWithValue",
                "groupIndex": 0,
                "groupName": "",
                "expressionsValue": "JSON",
                "expressions": {
                    "type": "FillEmptyWithValue",
                    "code": "pyspark",
                    "params": {
                        "columns": ["订单内件数"],
                        "value": "4"
                    }
                }
            },
        ]
    }
'''


def lambda_handler(event, context):
    phs3 = PhS3()
    name = f"{event['projectName']}_{event['dagName']}_{event['flowVersion']}"
    job_full_name = f"""{name}_{event["script"]["jobName"]}"""

    # 1 收集参数，转成想要的结构
    conf = {
        "s3": phs3,

        "bucket": os.environ["BUCKET"],
        "cliVersion": os.environ["CLI_VERSION"],
        "jobPathPrefix": os.environ["JOB_PATH_PREFIX"],
        "dagS3JobsPath": os.environ["DAG_S3_JOBS_PATH"],

        "steps": event["steps"],
        "traceId": event["traceId"],
        "projectId": event["projectId"],
        "projectName": event["projectName"],
        "dagName": event["dagName"],
        "flowVersion": event["flowVersion"],
        "jobFullName": job_full_name,
        "name": name,
        "jobPath": f"""{os.environ["JOB_PATH_PREFIX"]}{name}/{job_full_name}""",
        "input": event["script"]["inputs"][0]
    }

    with open('./code.yaml', encoding='utf-8') as file:
        conf["code_yaml"] = yaml.safe_load(file)
        # 生成低代码phjob核心逻辑
        create_ph_job_file(conf)

        # 将脚本上传到对应位置
        upload_file(conf)

    return {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {
                "script": event["script"]["jobName"]
            },
            "error": {}
        }
    }
