import json
import time

import boto3
from io import BytesIO
import gzip

def if_exit(bucket, key):
    _s3 = boto3.client('s3')
    try:
        response = _s3.get_object(Bucket=bucket, Key=key)
        return response.get('Body').read()
    except:
        return


def down_file(bucket, key, path):
    _s3 = boto3.client('s3')
    _s3.download_file(Filename=f"/tmp/{path}",
                      Bucket=bucket, Key=key)
    return True


def read_file(bucket, key):
    path = key.split('/')[-1]
    if down_file(bucket, key, path):
        filehandler = open("/tmp/"+path, "rb")
        filelines = filehandler.readlines()
        data = ''
        for i in filelines:
            data += i.decode("utf-8", "ignore")
        return data


def read_gz(gz_data):
    gzipfile = BytesIO(gz_data)
    return gzip.GzipFile(fileobj=gzipfile).read()


def query_logfile(bucket, file_key):
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(
        Bucket=f'{bucket}',
        Prefix=f'2020-11-11/emr/yarnLogs/hadoop/logs-tfile/{file_key}/',
        MaxKeys=100)
    return [i.get('Key') for i in response.get('Contents', {})]


def get_log_path(step_id, cluster_id):
    try:
        bucket = "ph-platform"
        key = f"2020-11-11/emr/logs/{cluster_id}/steps/{step_id}/stderr.gz"
        result = ""
        while 1:
            time.sleep(10)
            print("获取steplog")
            result = if_exit(bucket, key)
            if result:
                break
        print(result)
        if not result:
            return
        log_file = read_gz(result).decode()
        file_nmae = log_file[log_file.rfind('application_'): log_file.rfind('application_') + 30]
        print(file_nmae)
        logs = []
        if file_nmae:
            yarn_log_path = f"ph-platform/2020-11-11/emr/yarnLogs/hadoop/logs-tfile/{file_nmae}/"
            yarnLog = {
                "type": "yarnLog",
                "uri": yarn_log_path
            }
            logs.append(yarnLog)
        step_log = f"ph-platform/2020-11-11/emr/logs/{cluster_id}/steps/{step_id}/stderr.gz"
        stepLog = {
            "type": "stepLog",
            "uri": step_log
        }
        logs.append(stepLog)
        return json.dumps(logs, ensure_ascii=False)
    except:
        return