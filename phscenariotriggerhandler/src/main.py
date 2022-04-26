import os
import json
import boto3
import traceback


def lambda_handler(event, context):
    event = json.loads(event["body"])
    print(event)

    timer_cfn_path = "s3://ph-platform/2020-11-11/jobs/statemachine/pharbers/template/scenario-timer-cfn.yaml"

    # 1. 如果是创建
    

    return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
            },
            "body": json.dumps(result)
        }