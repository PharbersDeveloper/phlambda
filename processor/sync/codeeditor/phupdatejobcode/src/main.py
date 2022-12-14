import json
import json
import boto3
import datetime
import time
import urllib
from urllib import parse


def down_data_with_time(bucket, key, file_name, **kwargs) -> tuple:
    client = boto3.client('s3')
    response = client.get_object(Bucket=bucket, Key=(key+file_name))
    binaryarray = response.get('Body').read().decode()
    last_time = response.get('LastModified')
    return binaryarray, int(time.mktime(last_time.timetuple()))+3600*8


def up_data(bucket, key, file_name, data):
    data = urllib.parse.unquote(data)
    s3 = boto3.client('s3')
    s3.put_object(Body=data.encode(), Bucket=bucket, Key=(key+file_name))


def run(timespan, **kwargs):
    data, last_time = down_data_with_time(**kwargs)
    print(last_time)
    print(data)

    if int(timespan) > last_time:
        up_data(**kwargs)
        return ['up data success', 1]
    else:
        return ['timespan error', 0]


def lambda_handler(event, context):
    try:
        result, status = run(**eval(event["body"]))

    except Exception as e:
        return {
            "statusCode": 503,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": str(e)})
        }
    else:
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": result, "status": status})
        }


