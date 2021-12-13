import json
import boto3
from hashlib import md5


def read_s3(bucket, key, file_name, **kwargs) -> tuple:
    is_type = lambda type_name: type_name.split('.')[1]
    rank_md5 = lambda rank_obj: md5(rank_obj.encode()).hexdigest()

    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=(key + file_name))

    refer_name = f"{rank_md5(file_name+response['ETag']+str(response['LastModified']))}.{is_type(file_name)}"
    s3.download_file(Filename=f"/Users/moke/worker_space/phlambda/phdatodfs/{refer_name}",
                     Bucket=bucket, Key=(key+file_name))

    return refer_name, file_name


def lambda_handler(event, context):

    try:
        refer_name, file_name = read_s3(**eval(event["body"]))
        print(refer_name, file_name)

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
            "body": json.dumps({"message": {"refer_name": refer_name, "file_name": file_name}}, ensure_ascii=False)
        }
