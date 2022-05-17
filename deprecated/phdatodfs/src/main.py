import json
import boto3
import time
from hashlib import md5


def read_s3(bucket, key, file_name, projectId, **kwargs) -> tuple:
    is_type = lambda type_name: type_name.split('.')[1]
    rank_md5 = lambda rank_obj: md5(rank_obj.encode()).hexdigest()

    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=(key + file_name))
    print(projectId)

    refer_name = f"{rank_md5(file_name+response['ETag']+str(response['LastModified']))+str(int(time.time()))}.{is_type(file_name)}"
    s3.download_file(Filename=f"/mnt/tmp/{projectId}/tmp/{refer_name}",
                     Bucket=bucket, Key=(key+file_name))

    return refer_name, file_name


def lambda_handler(event, context):

    try:
        refer_name, file_name = read_s3(**eval(event["body"]))
        print(refer_name, file_name)
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": {"refer_name": refer_name, "file_name": file_name}, "status": 1}, ensure_ascii=False)
        }


    except Exception as e:
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": str(e), "status": 0}, ensure_ascii=False)
        }
