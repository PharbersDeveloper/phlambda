import boto3
import json


s3 = boto3.client('s3')


def if_exit(bucket, key):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return response.get('Body').read()
    except:
        return


def run(path):
    key = path.split("//")
    bucket = key[1].split("/")[0]
    key = key[1][len(bucket)+1:]
    return json.loads(if_exit(bucket, key))


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
