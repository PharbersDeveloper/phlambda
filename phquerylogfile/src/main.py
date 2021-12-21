import json
import boto3
from io import BytesIO
import gzip
import base64


s3 = boto3.client('s3')
def if_exit(bucket, key):
    _s3 = boto3.client('s3')
    try:
        response = _s3.get_object(Bucket=bucket, Key=key)

        return response.get('Body').read()
    except:
        return


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
    result = if_exit(bucket, key+"stderr.gz")
    if not result:
        return
    log_file = read_gz(result).decode()
    file_nmae = log_file[log_file.rfind('application_'): log_file.rfind('application_')+30]
    logkey_list = query_logfile(bucket, file_nmae)

    # with open('test1.txt', 'wb') as f:
    #     for i in logkey_list:
    #         f.write(if_exit(bucket, i))
    # for i in logkey_list:
    #     reasult = if_exit(bucket, i)
    #     base64_data = base64.b64encode(reasult)
    #     print(json.dumps(base64_data))
    #     print(type(base64_data))
    #     base64_str = base64_data.decode('utf-8')
    return [base64.b64encode(if_exit(bucket, i)).decode('utf-8') for i in logkey_list]


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
