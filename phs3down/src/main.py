import json
import boto3


def down(key):
    print(key)
    s3 = boto3.client('s3')
    return s3.generate_presigned_url('get_object', Params={'Bucket': 'ph-platform', 'Key': key},
                                     ExpiresIn=3600, HttpMethod="get")


def query_logfile(bucket, key):
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(
        Bucket=f'{bucket}',
        Prefix=key,
        MaxKeys=100)
    return [i.get('Key') for i in response.get('Contents', {})]


def run(event):
    body = eval(event['body'])
    key = query_logfile(**body)
    if key:
        return down(key[0])


def lambda_handler(event, context):

    try:
        result = run(event)
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
                "body": json.dumps({"message": result, "status": 0}, ensure_ascii=False)
            }


    except Exception as e:
        return {
            "statusCode": 503,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": str(e)}, ensure_ascii=False)
        }

