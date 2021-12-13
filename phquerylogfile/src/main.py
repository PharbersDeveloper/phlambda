import json
import boto3
from io import BytesIO
import gzip


def if_exit(bucket, key):
    _s3 = boto3.client('s3')
    try:
        response = _s3.get_object(Bucket=bucket, Key=key+"stderr.gz")
        print(response)
    except:
        return False
    else:
        return True


def read_s3(bucket, key, **kwargs):
    if not if_exit(bucket, key):
        return

    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key+"stderr.gz")
    n = obj.get()['Body'].read()
    gzipfile = BytesIO(n)
    gzipfile = gzip.GzipFile(fileobj=gzipfile)
    content = gzipfile.read()
    # print(content.decode())
    return content.decode()


def lambda_handler(event, context):
    try:
        data = read_s3(**eval(event["body"]))
        if not data:
            return {
                        "statusCode": 200,
                        'headers': {
                            'Access-Control-Allow-Origin': '*'
                        },
                        "body": json.dumps({"message": "error", "status": 0}, ensure_ascii=False)
                    }
        rdata = data[data.rfind('application_'): data.rfind('application_')+30]
        print(rdata)

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
            "body": json.dumps({"message": rdata, "status": 1}, ensure_ascii=False)
        }
