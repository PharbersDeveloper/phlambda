import boto3
import json


s3 = boto3.client('s3')


def get_data(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    return json.loads(response.get('Body').read())


def query_file(bucket, file_key):
    response = s3.list_objects_v2(
        Bucket=f'{bucket}',
        Prefix=file_key,
        MaxKeys=100)
    return [i.get('Key') for i in response.get('Contents', {})]


def run(path, **kwargs):
    result_dict = {}
    key = path.split("//")
    bucket = key[1].split("/")[0]
    file_key = key[1][len(bucket)+1:]
    for key in query_file(bucket, file_key=file_key):
        result_dict[key.split("/")[-1]] = get_data(bucket, key)
    return result_dict


def lambda_handler(event, context):
    try:
        data = run(**eval(event["body"]))
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": data, "status": 0}, ensure_ascii=False)
        }

    except Exception as e:
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": str(e), "status": 1}, ensure_ascii=False)
        }
