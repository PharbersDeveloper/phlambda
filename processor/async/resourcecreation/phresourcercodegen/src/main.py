import os
import json
import yaml
import subprocess
from string import Template
from util.AWS.ph_s3 import PhS3


'''
创建pyspark
args = {
    "traceId": "String",
    "projectId": "String",
    "owner": "String",
    "showName": "String",
    "dagName": "String",
    "owner": "String",
    "projectName": "String",
    "script": {
        "id": "String",
        "runtime": "String",
        "name": "String",
        "flowVersion": "developer",
        "inputs": "[]",
        "output": "{}"
    }
}
'''


class RTemplate(Template):
    delimiter = "$$"


def write_file(path, data):
    with open(path, "w") as file:
        file.write(data)


def upload_file(bucket, key, path):
    PhS3().upload_dir(
        dir=path,
        bucket_name=bucket,
        s3_dir=key
    )


def lambda_handler(event, context):
    print(event)

    if event["script"].get("name"):
        inputs = json.loads(event["script"]["inputs"])
        args = {
            "inputs": ", ".join(list(map(lambda item: f"'{item}'", inputs))),
            "output": event["script"]["output"],
            "project_id": event["projectId"],
            "project_name": event["projectName"],
            "runtime": event["script"]["runtime"],
            "dag_name": event["dagName"],
            "script_name": event["script"]["name"],
            "input_var_args": "\n\t\t".join(list(map(lambda ds: f"""data_frame <- cmd_args[["df_{ds}"]]""", inputs))) \
                .replace("\t", "     ")
        }
        name = f"{event['projectName']}_{event['dagName']}_{event['script']['flowVersion']}"
        job_full_name = f"""{name}_{event["script"]["name"]}"""
        jobPath = f"""{os.environ["JOB_PATH_PREFIX"]}{name}/{job_full_name}"""

        # 创建目录
        subprocess.call(["mkdir", "-p", jobPath])
        # 创建 TraceId File
        subprocess.call(["touch", jobPath + "/" + event["traceId"]])

        with open('./code.yaml', encoding='utf-8') as file:
            result = yaml.safe_load(stream=RTemplate(file.read()).substitute(args))
            write_file(f"{jobPath}/phmain.R", result["code"]["phmain"]["code"])
            write_file(f"{jobPath}/phjob.R", result["code"]["phjob"]["code"].replace("\t", "    "))
            s3_path_key = f"""{os.environ["CLI_VERSION"]}{os.environ["DAG_S3_JOBS_PATH"]}{name}/{job_full_name}"""
            upload_file(os.environ["BUCKET"], s3_path_key, jobPath)
    return event["script"]
