import json
import time

import boto3
from io import BytesIO
import gzip
import base64


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


def run(bucket, key, **kwargs):
    try:
        result = if_exit(bucket, key + "stderr.gz")
        print(result)
        if not result:
            return
        log_file = read_gz(result).decode()
        file_nmae = log_file[log_file.rfind('application_'): log_file.rfind('application_') + 30]
        print(file_nmae)
        logkey_list = query_logfile(bucket, file_nmae)
        print(logkey_list)

        data = ""
        for i in logkey_list:
            data += read_file(bucket, i)
        return data
    except:
        return


def lambda_handler(event, context):
    try:
        data = run(**eval(event["body"]))
        if not data:
            return {
                "statusCode": 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                "body": json.dumps({"message": "error", "status": 0}, ensure_ascii=False)
            }
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": data, "status": 1}, ensure_ascii=False)
        }

    except Exception as e:
        return {
            "statusCode": 503,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": str(e), "status": 0}, ensure_ascii=False)
        }

