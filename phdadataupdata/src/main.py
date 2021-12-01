import json
import boto3
import datetime
import time


def down_data_with_time(bucket, key, file_name, **kwargs) -> tuple:
    client = boto3.client('s3')
    response = client.get_object(Bucket=bucket, Key=(key+file_name))
    binaryarray = response.get('Body').read().decode()
    last_time = response.get('LastModified')
    print(response)
    print(last_time)
    return binaryarray, int(time.mktime(last_time.timetuple()))+3600*8


def up_data(bucket, key, file_name, data):
    # s3 = boto3.client('s3')
    # s3.put_object(Body=data.encode(), Bucket=bucket, Key=(key+file_name))
    print(1)


def run(timespan, **kwargs):
    data, last_time = down_data_with_time(**kwargs)
    print(last_time)
    print(data)

    if int(timespan) > last_time:
        up_data(**kwargs)
        return 'up data success'
    else:
        return 'timespan error'


def lambdaHandler(event, context):

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE"
        },
        "body": run(**eval(event["body"]))
    }


