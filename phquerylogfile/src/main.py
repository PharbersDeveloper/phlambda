import json
import boto3
from io import BytesIO
import gzip
import base64


s3 = boto3.client('s3')
def if_exit(bucket, key):
    # response = s3.get_object(Bucket='ph-platform',
    #                          Key='2020-11-11/emr/yarnLogs/hadoop/logs-tfile/application_1639098106143_0120/ip-192-168-27-243.cn-northwest-1.compute.internal_8041')
    # a = response.get('Body').read()
    # print(a)
    _s3 = boto3.client('s3')
    try:
        response = _s3.get_object(Bucket=bucket, Key=key)
    except:
        return False
    else:
        base64_data = base64.b64encode(response.get('Body').read())
        base64_str = base64_data.decode('utf-8')
        return base64_str


def read_gz(bucket, key):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)
    gzipfile = BytesIO(obj.get()['Body'].read())
    return gzip.GzipFile(fileobj=gzipfile).read()


def query_logfile(bucket, file_key):
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(
        Bucket=f'{bucket}',
        Prefix=f'2020-11-11/emr/yarnLogs/hadoop/logs-tfile/{file_key}/',
        MaxKeys=100)
    return [i.get('Key') for i in response.get('Contents', {})]


def run(bucket, key, **kwargs):
    if not if_exit(bucket, key+"stderr.gz"):
        return
    log_file = read_gz(bucket, key+"stderr.gz").decode()
    file_nmae = log_file[log_file.rfind('application_'): log_file.rfind('application_')+30]
    logkey_list = query_logfile(bucket, file_nmae)

    # with open('test1.txt', 'wb') as f:
    #     for i in logkey_list:
    #         f.write(if_exit(bucket, i))

    return [if_exit(bucket, i) for i in logkey_list]


def lambda_handler(event, context):
    try:
        data = run(**eval(event["body"]))
        print(data)
        if not data:
            return {
                        "statusCode": 200,
                        'headers': {
                            'Access-Control-Allow-Origin': '*'
                        },
                        "body": json.dumps({"message": "error", "status": 0}, ensure_ascii=False)
                    }

    # application_1639098106143_0120
    except Exception as e:
        return {
            "statusCode": 503,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": str(e), "status": 0}, ensure_ascii=False)
        }
    else:
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": data, "status": 1}, ensure_ascii=False)
        }
    # data = run(**eval(event["body"]))
    # print(data)