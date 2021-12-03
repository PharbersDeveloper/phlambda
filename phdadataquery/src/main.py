import json
import boto3
import time


def down_data_with_time(bucket, key, file_name, **kwargs) -> tuple:
    client = boto3.client('s3')
    response = client.get_object(Bucket=bucket, Key=(key+file_name))
    binaryarray = response.get('Body').read().decode()
    last_time = response.get('LastModified')
    print(response)
    print(last_time)
    return binaryarray, int(time.mktime(last_time.timetuple()))+3600*8


# def up_data(bucket, key, file_name, data):
    # s3 = boto3.client('s3')
    # s3.put_object(Body=data.encode(), Bucket=bucket, Key=(key+file_name))
    # print(1)


def run(**kwargs):
    data, last_time = down_data_with_time(**kwargs)
    return {"data": data, "timespan": last_time}


def lambda_handler(event, context):
    try:
        result = run(**eval(event["body"]))

    except Exception as e:
        return {
            "statusCode": 503,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": str(e)}, ensure_ascii=False)
        }
    else:
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": result}, ensure_ascii=False)
        }
