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

args = {
    "traceId": "automax_automax_developer_2022-05-24T02%3A01%3A19+00%3A00_袁毓蔚",
    "projectId": "s7nBDbpqfUShq1w",
    "owner": "String",
    "showName": "String",
    "dagName": "hospital_mapping_out",
    "owner": "String",
    "projectName": "automax",
    "scripts": {
        "id": "String",
        "runtime": "String",
        "name": "sync_test",
        "flowVersion": "developer",
        "inputs": "['automax_automax_developer_2022-05-26T01:45:57+00:00_袁毓蔚']",
        "output": "test_out_hospital_mapping_out"
    },
}
'''
projectId = args['projectId']
dagName = args['dagName']
out_table = args['scripts']['output']
out_version = args['scripts']['inputs']
flowVersion = args['scripts']['flowVersion']
scripts_name = args['scripts']['name']
projectName = args['projectName']

# 读取yaml文件
template_yaml = open('template.yaml', 'r', encoding='utf-8').read()
template_yaml = yaml.load(template_yaml, Loader=yaml.FullLoader)

# 获取phjob.py 模板
phjob_script = template_yaml['template']['phjob.py']['content'] \
                    .replace("$projectId", f"'{projectId}'") \
                    .replace("$dagName", f"'{dagName}'") \
                    .replace("$out_table", f"'{out_table}'") \
                    .replace("$out_version", out_version) \
                    .replace("$version_col", f"'traceId'") \
                    .replace("$lack_path", f"'s3://ph-platform/2020-11-11/lake/pharbers'")
# 获取phmain.py 模板
phmain_script = template_yaml['template']['phmain.py']['content']  

# 写出到s3
def getScriptPathKey(projectName, flowVersion, scripts_name):
    return f"2020-11-11/jobs/python/phcli/{projectName}_{projectName}_{flowVersion}/{projectName}_{projectName}_{flowVersion}_{scripts_name}"

def toS3(script, filename):
    script_bytes = str.encode(script)
    client = boto3.client('s3')
    response = client.put_object(
        Body = script_bytes,
        Bucket='ph-platform',
        Key=f"{getScriptPathKey(projectName, flowVersion, scripts_name)}/{filename}") 
    
toS3(phjob_script, "phjob.py")
toS3(phmain_script, "phmain.py")
