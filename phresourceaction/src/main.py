import os, sys
import logging
import json

from getResourceStatus import GetResourceStatus


def execute(resource_type, event):
    # 如果是start 先判断在ssm 的 resource_status中是否有该resource 如果没有或者status为closed更新status为starting
    # 如果存在并且status不是closed直接返回状态
    status = GetResourceStatus(resource_type=resource_type, event=event).execute()

    return status


def lambda_handler(event, context):
    result_code = 200
    result_message = {}
    try:
        event = event['body']
        if type(event) == str:
            event = json.loads(event)
        resource_type = event.get("content_type")
        status = execute(resource_type, event)
        result_message = {
            "status": "ok",
            "data": {
                "resource_status": status
            }
        }
    except Exception as e:
        result_message = {
            "status": "error",
            "data": {
                "message": "resource start failure: " + str(e)
            }
        }

    if result_message["status"] == "error":
        result_code = 503

    return {
        "statusCode": result_code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE"
        },
        "body": json.dumps(result_message)
    }

if __name__ == '__main__':
    with open("../events/event_create_resource.json") as f:
        event = json.load(f)
    lambda_handler(event, context=0)