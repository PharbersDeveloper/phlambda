import os
import yaml
import subprocess
from string import Template
from PhS3 import PhS3

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
            "jobName": "compute_BB",
            "runtime": "topn",
            "jobPath": "",
            "inputs": ["AA"],           // 现在没用，可能以后有用
            "outputs": [],            // 现在没用，可能以后有用
            "id": "001"
        },
        "steps": [                  // 这个地方特别需要注意，直接传最后需要保存的样子，（跳出删除修改插入的思想死循环）
            {
                "id": "alextest_demo_demo_developer_compute_十多个",
                "stepId": "1",
                "index": "1",
                "runtime": "join",
                "stepName": "Initial Join",
                "ctype": "JOIN",
                "groupIndex": 0,
                "groupName": "",
                "expressionsValue": "JSON",
                "expressions": {}
            },
        ]
    }
'''


def write_file(path, data):
    with open(path, "w") as file:
        file.write(data)


def upload_file(bucket, key, path):
    PhS3().upload(
        file=path,
        bucket_name=bucket,
        object_name=key
    )


def lambda_handler(event, context):
    print(event)
    args = {
        "inputs": event["script"]["inputs"],
        "join_args": event["steps"][0]["expressions"]["params"],
        "project_id": event["projectId"],
        "job_id": event["steps"][0]["id"].split("_")[-1]
    }
    name = f"{event['projectName']}_{event['dagName']}_{event['flowVersion']}"
    job_full_name = f"""{name}_{event["script"]["jobName"]}"""
    jobPath = f"""{os.environ["JOB_PATH_PREFIX"]}{name}/{job_full_name}"""

    # 创建目录
    subprocess.call(["mkdir", "-p", jobPath])
    # 创建 TraceId File
    subprocess.call(["touch", jobPath + "/" + event["traceId"]])

    with open("./code.yaml", encoding="utf-8") as file:
        file_name = "phjob.py"
        result = yaml.safe_load(stream=Template(file.read()).substitute(args))
        write_file(f"{jobPath}/{file_name}", result["code"]["phjob"]["code"])
        s3_path_key = f"""{os.environ["CLI_VERSION"]}{os.environ["DAG_S3_JOBS_PATH"]}{name}/{job_full_name}"""
        upload_file(os.environ["BUCKET"], f"{s3_path_key}/{file_name}", f"{jobPath}/{file_name}")
        upload_file(os.environ["BUCKET"], f"{s3_path_key}/{event['traceId']}", f"{jobPath}/{event['traceId']}")

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
