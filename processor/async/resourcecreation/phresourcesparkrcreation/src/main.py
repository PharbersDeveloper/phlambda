import os
import json
import subprocess
from phtraceid import *
from phmain import *
from phjob import *
from upload2s3 import *
from util.ph_s3 import PhS3

'''
创建pyspark
args = {
    "traceId": "String",
    "projectId": "String",
    "owner": "String",
    "showName": "String",
    "projectName": "String",
    "dagName": "String",
    "jobDisplayName": "String",
    "scripts": {
        "id": "String",
        "jobName": "String",
        "actionName": "String",
        "flowVersion": "developer",
        "inputs": "[{"name": ""}]",
        "output": "{"name": ""}"
    }
}
args = {
    "traceId": "alfred-resource-creation-traceId",
    "dagName": "demo",
    "owner": "alex_qian_00001",
    "showName": "钱鹏",
    "projectName": "demo",
    "projectId": "ggjpDje0HUC2JW",
    "script": {
        "name": "compute_BB",
        "flowVersion": "developer",
        "runtime": "r",
        "inputs": "[\"AA\"]",
        "output": "BB",
        "id": "001"
    }
}
'''


def lambda_handler(event, context):
    print(event)

    if event["script"]["runtime"] == "dataset" and "name" not in event["script"]:
        return event["script"]
    # 创建R代码的流程
    try:
        phs3 = PhS3()
        name = f"{event['projectName']}_{event['dagName']}_{event['script']['flowVersion']}"
        job_full_name = f"""{name}_{event["script"]["name"]}"""

        # 1 收集参数，转成想要的结构
        conf = {
            "s3": phs3,

            "bucket": os.environ["BUCKET"],
            "cliVersion": os.environ["CLI_VERSION"],
            "jobPathPrefix": os.environ["JOB_PATH_PREFIX"],
            "templatePhmainFile": os.environ["TM_PHMAIN_FILE"],
            "templatePhjobFile": os.environ["TM_PHJOB_FILE"],
            "dagS3JobsPath": os.environ["DAG_S3_JOBS_PATH"],

            "traceId": event["traceId"],
            "projectId": event["projectId"],
            "projectName": event["projectName"],
            "dagName": event["dagName"],
            "flowVersion": event["script"]["flowVersion"],
            "jobFullName": job_full_name,
            "inputs": json.loads(event["script"]["inputs"]),
            "output": event["script"]["output"],
            "name": name,
            "jobPath": f"""{os.environ["JOB_PATH_PREFIX"]}{name}/{job_full_name}"""
        }

        # os.system("rm -rf " + conf.get("jobPath") + "/*")
        subprocess.call(["mkdir", "-p", conf.get("jobPath")])

        create_ph_trace_id_file(conf)

        # 2 生成ph_main.R文件
        create_ph_main_file(conf)
        # 3 生成ph_job.R文件
        create_ph_job_file(conf)
        # 4 上传到S3对应的位置
        upload_files(conf)
        return event["script"]
    except Exception as e:
        raise Exception(f"creation spark r file error, detail: {str(e)}")

