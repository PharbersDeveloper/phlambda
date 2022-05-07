import os
import json
import subprocess
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
'''


def lambda_handler(event, context):

    # 创建R代码的流程

    try:
        phs3 = PhS3()
        name = f"{event['projectName']}_{event['dagName']}_{event['scripts']['flowVersion']}"

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
            "flowVersion": event["scripts"]["flowVersion"],
            "jobDisplayName": event["jobDisplayName"],
            "inputs": json.loads(event["scripts"]["inputs"]),
            "output": json.loads(event["scripts"]["output"])["name"],
            "name": name,
            "jobPath": os.environ["JOB_PATH_PREFIX"] + name + "/" + event["jobDisplayName"]
        }

        os.system("rm -rf " + conf.get("jobPath") + "/*")
        subprocess.call(["mkdir", "-p", conf.get("jobPath")])

        # 2 生成ph_main.R文件
        create_ph_main_file(conf)
        # 3 生成ph_job.R文件
        create_ph_job_file(conf)
        # 4 上传到S3对应的位置
        upload_files(conf)

        return True
    except Exception as e:
        raise Exception(f"creation sparkr file error, detail: {str(e)}")
