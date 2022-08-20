import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
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


def lambda_handler(event, context):
    print(event)
    # 删除codebuild
    # 
    return 1
