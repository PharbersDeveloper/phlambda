import json
import time

import asyncio
import boto3
from io import BytesIO
import gzip
import base64

s3 = boto3.client('s3')


def if_exit(bucket, key):

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return response.get('Body').read()
    except:
        return


def read_file(bucket, key):
    path = key.split('/')[-1]
    s3.download_file(Filename=f"/tmp/{path}",
                     Bucket=bucket, Key=key)
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
    try:
        response = s3.list_objects_v2(
            Bucket=f'{bucket}',
            Prefix=f'2020-11-11/emr/yarnLogs/hadoop/logs-tfile/{file_key}/',
            MaxKeys=100)
        return [i.get('Key') for i in response.get('Contents', {})]
    except:
        return


def run(bucket, key, **kwargs):

    count = 0
    result = None
    logkey_list = None
    data = ""

    while not result:
        time.sleep(30)
        result = if_exit(bucket, key + "stderr.gz")
        count += 1
        if count == 30:
            raise

    log_file = read_gz(result).decode()
    file_nmae = log_file[log_file.rfind('application_'): log_file.rfind('application_') + 30]
    print(file_nmae)

    while not logkey_list:
        logkey_list = query_logfile(bucket, file_nmae)
        time.sleep(30)
        count += 1
        if count == 30:
            raise

    for i in logkey_list:
        data += read_file(bucket, i)
    return data


def lambda_handler(event, context):
    try:
        data = run(**eval(event["body"]))
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
