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


def create_cloudfront_invalidation(bucket, keys):
    response = cloudfront_client.list_distributions()

    items = response["DistributionList"]["Items"]
    for item in response["DistributionList"]["Items"]:
        for i in item["Origins"]["Items"]:
            if i.get("DomainName").startswith(bucket):
                distribution_id = item.get("Id")
    print(distribution_id)

    cloudfront_client.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            'Paths': {
                'Quantity': len(keys),
                'Items': keys
            },
            'CallerReference': str(math.floor(datetime.datetime.now().timestamp() * 1000))
        }
    )


def lambda_handler(event, context):
    print(event)
    # 获取上传到s3的文件路径
    if event["invalidate"]:
        deploy_s3_paths = event["deployS3Paths"]
        invalidations_maps = {}
        buckets = list(set(map(lambda x: x["bucket"], deploy_s3_paths)))
        for bucket in buckets:
            invalidations_maps.update({bucket: []})
        for deploy_s3_path in deploy_s3_paths:
            invalidations_maps[deploy_s3_path["bucket"]].append("/" + deploy_s3_path["key"])
        for bucket, keys in invalidations_maps.items():
            create_cloudfront_invalidation(bucket=bucket, keys=keys)
    return 1
