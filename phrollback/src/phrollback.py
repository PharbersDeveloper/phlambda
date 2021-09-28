import boto3


def bulid_prefix_of_files(prefix_of_path,provider,version,owner):
    import os

    prefix_of_files = f"provider={provider}/"+f"version={version}/"+f"owner={owner}"

    prefix_of_files = os.path.join(str(prefix_of_path),prefix_of_files)

    print(prefix_of_files)

    return prefix_of_files

def rollback(bucket_name,prefix_of_files,provider,version,owner):

    s3 = boto3.resource('s3','cn-northwest-1')
    bucket = s3.Bucket(bucket_name)

    prefix_of_path = bulid_prefix_of_files(prefix_of_files,provider,version,owner)

    response = bucket.objects.filter(Prefix=prefix_of_path).delete()

    print(response)
    return response


def lambda_handler(event,context):

    import json

    event = json.loads(event['body'])

    event = event['parameters']['click_event']

    provider = event["provider_name"]
    version = event["version_name"]
    owner = event["owner_name"]

    bucket_name = "ph-platform"
    prefix_of_files = "2020-11-11/etl/readable_files/clean_source/"
    response = rollback(bucket_name, prefix_of_files, provider, version, owner)

    response = response[0]['ResponseMetadata']

    statusCode = response['HTTPStatusCode']


    return {
            'statusCode': statusCode,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
            },
            'body': json.dumps({
            'ResponseMetadata': response,
            })
        }


