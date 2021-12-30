import json
import boto3
import time


def down(key):
    print(key)
    s3 = boto3.client('s3')
    return s3.generate_presigned_url('get_object', Params={'Bucket': 'ph-platform', 'Key': key},
                                     ExpiresIn=3600, HttpMethod="get")


def copy_file(dataset_name, key, **kwargs):
    current_time = time.strftime("%Y%m%d%H%M%S")
    file_type = key[key.rfind('.'):]
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket='ph-platform', Key=key)["Body"].read().decode()
    s3.put_object(Bucket='ph-platform', Key=f'2020-11-11/download/{dataset_name}_{current_time}{file_type}',
                  Body=response)
    return f'2020-11-11/download/{dataset_name}_{current_time}{file_type}'


def query_logfile(bucket, path, **kwargs):
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(
        Bucket=f'{bucket}',
        Prefix=path,
        MaxKeys=100)
    print(response)
    return [i.get('Key') for i in response.get('Contents', {})]


def run(event):
    body = eval(event['body'])
    file_list = query_logfile(**body)
    print(file_list)
    if len(file_list) > 1:
        key = copy_file(key=file_list[1], **body)
        return down(key)


def lambda_handler(event, context):

    try:
        result = run(event)
        print(result)
        if result:
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                },
                "body": json.dumps({"message": result, "status": 1}, ensure_ascii=False)
            }
        else:
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                },
                "body": json.dumps({"message": "Missing required files!", "status": 0}, ensure_ascii=False)
            }

    except Exception as e:
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": str(e), "status": 0}, ensure_ascii=False)
        }
