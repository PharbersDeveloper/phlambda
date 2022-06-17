import json
import os
import yaml
import boto3

'''
创建 sync
args = {
    "traceId": "String",
    "projectId": "String",
    "owner": "String",
    "showName": "String",
    "dagName": "String",
    "owner": "String",
    "projectName": "String",
    "scripts": {
        "id": "String",
        "runtime": "String",
        "name": "String",
        "flowVersion": "developer",
        "inputs": "[]",
        "output": "{}"
    },
}

'''

event = {
    "traceId": "automax_automax_developer_2022-05-24T02%3A01%3A19+00%3A00_袁毓蔚",
    "projectId": "ggjpDje0HUC2JW",
    "owner": "String",
    "showName": "String",
    "dagName": "demo",
    "owner": "String",
    "projectName": "demo",
    "script": {
        "id": "String",
        "runtime": "syncfiles",
        "name": "compute_yyw",
        "flowVersion": "developer",
        "inputs": "[\"A\"]",
        "output": "yyw",
        "version": "[]",
    },
}


def lambda_handler(event, context):
    args = event
    projectId = args['projectId']
    projectName = args['projectName']
    dagName = args['dagName']
    scripts_name = args['script']['name']
    output = args['script']['output']
    inputs = args['script']['inputs']
    inputs = json.loads(inputs)[0]
    version = args['script']['version']
    flowVersion = args['script']['flowVersion']
    projectName = args['projectName']
    args_scripts = args['script']
    runtime = args['script']['runtime']

    # 读取yaml文件
    template_yaml = open('template.yaml', 'r', encoding='utf-8').read()
    template_yaml = yaml.load(template_yaml, Loader=yaml.FullLoader)

    # 获取phjob.py 模板
    phjob_script = template_yaml['template']['phjob.py']['content'] \
                        .replace("$inputs$", str(inputs)) \
                        .replace("$version$", str(version))

    # 获取phmain.py 模板
    phmain_script = template_yaml['template']['phmain.py']['content'] \
                        .replace("$dag_name", dagName) \
                        .replace("$project_id", projectId) \
                        .replace("$project_name", projectName) \
                        .replace("$script_name", scripts_name) \
                        .replace("$runtime", runtime) \
                        .replace("$output", output) \
                        .replace("$inputs", str(args['script']['inputs']))


    # 写出到s3
    def getScriptPathKey(projectName, flowVersion, output):
        return f"2020-11-11/jobs/python/phcli/{projectName}_{projectName}_{flowVersion}/{projectName}_{projectName}_{flowVersion}_{output}"

    def toS3(script, projectName, flowVersion, scripts_name, filename):
        script_bytes = str.encode(script)
        client = boto3.client('s3')
        response = client.put_object(
            Body = script_bytes,
            Bucket='ph-platform',
            Key=f"{getScriptPathKey(projectName, flowVersion, scripts_name)}/{filename}") 

    toS3(phjob_script, projectName, flowVersion, scripts_name, "phjob.py")
    toS3(phmain_script, projectName, flowVersion, scripts_name, "phmain.py")
    
    return args['script']

