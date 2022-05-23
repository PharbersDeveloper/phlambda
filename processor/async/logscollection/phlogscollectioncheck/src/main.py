import json
import boto3
from io import BytesIO
import gzip
from datetime import datetime, timedelta

_s3 = boto3.client('s3')
waitTotal = timedelta(hours=1)


'''
这个函数是对所有的personal resouce boot 的 clean up
args = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "clusterId": "",
    "stepId": ""
}

return:
    result = {
        "logIsReady": false,
        "stepLogPath": "",
        "YarLogPath": "",
        "LambdaLogPath": ""
    }
'''


def if_exit(bucket, key):    
    try:
        response = _s3.get_object(Bucket=bucket, Key=key, Range='bytes=0-9')
        return response.get('Body').read()
    except:
        return


def read_gz(gz_data):
    gzipfile = BytesIO(gz_data)
    return gzip.GzipFile(fileobj=gzipfile).read()


# 1. stackName 存在就删除
def lambda_handler(event, context):
    cluster_id = event["clusterId"]
    step_id = event["step_id"]

    waitUntil = event["date"] + waitTotal
    if datetime.now() > waitUntil:
        raise Exception("logs collections timeout")

    result = {
        "logIsReady": False,
        "stepLog": "",
        "yarnLog": "",
        "lambdaLog": ""
    }

    bucket = "ph-platform"
    key = f"2020-11-11/emr/logs/{cluster_id}/steps/{step_id}/stderr.gz"
    
    result["logIsReady"] = if_exit(bucket, key)
    
    print(result)
    if result["logIsReady"]:
        log_file = read_gz(result).decode()
        file_name = log_file[log_file.rfind('application_'): log_file.rfind('application_') + 30]
        print(file_name)
        if file_name:
            result["yarnLog"] = f"ph-platform/2020-11-11/emr/yarnLogs/hadoop/logs-tfile/{file_name}/"
            result["stepLog"] = f"ph-platform/2020-11-11/emr/logs/{cluster_id}/steps/{step_id}/stderr.gz"
        
    return result
