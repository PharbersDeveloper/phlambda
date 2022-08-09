import boto3
import math
import datetime

from boto3.dynamodb.conditions import Key
cloudfront_client = boto3.client('cloudfront')
'''

args:
    event = {
        "common": {
            "version": "version",
            "commit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
            "publisher": "赵浩博",
            "alias": "hbzhao-resource-change-position-owner",
            "runtime": "dev/v2/prod"
        }
    }
'''


def create_cloudfront_invalidation(bucket, key):
    response = cloudfront_client.list_distributions()

    items = response["DistributionList"]["Items"]
    for item in response["DistributionList"]["Items"]:
        for i in item["Origins"]["Items"]:
            # print(i)
            if i.get("DomainName").startswith(bucket):
                distribution_id = item.get("Id")

    print(distribution_id)
    cloudfront_client.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            'Paths': {
                'Quantity': 2,
                'Items': [
                    "/index.html",
                    "/robots.txt",
                ]
            },
            'CallerReference': str(math.floor(datetime.datetime.now().timestamp() * 1000))
        }
    )

def lambda_handler(event, context):
    print(event)
    # 获取上传到s3的文件路径
    deploy_s3_paths = event["deploy_s3_paths"]
    for s3_path_map in deploy_s3_paths:
        create_cloudfront_invalidation(bucket=s3_path_map["bucket"], key="/" + s3_path_map["key"])
    return 1
