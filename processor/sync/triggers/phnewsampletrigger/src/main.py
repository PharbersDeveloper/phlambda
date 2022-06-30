import os
import json
import boto3
import traceback


def lambda_handler(event, context):
    # 06301730
    print("phnewsampletrigger")
    result = {}
    result["message"] = "phnewsampletrigger success 1700"
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(result)
    }
