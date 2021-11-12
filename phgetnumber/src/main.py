import json
from src.util.AWS.DynamoDB import DynamoDB

import base64
from util.AWS.STS import STS
from constants.Common import Common

sts = STS().assume_role(
    base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
    "Ph-Back-RW"
)


def lambda_handler(event, context):
    try:
        body = eval(event["body"])
        dynamodb = DynamoDB(sts=sts)
        result = dynamodb.getTableCount(body["tableName"], body["projectId"])
    except Exception as e:
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": {"message": str(e)}})
        }
    else:
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": result})
        }


{"content_type": "test",
 "target_address": ["2091038466@qq.com"],
 "subject": "密码修改",
 "attachments": [{"file_name": "test1.yaml",    "file_context": ["PH_NOTICE_EMAIL:", "metadata:", "name: PH_NOTICE_EMAIL"]},
                 {"file_name": "test2.txt", "file_context": ["xxxxxxxxxxxxxxxxxx"]}]}
