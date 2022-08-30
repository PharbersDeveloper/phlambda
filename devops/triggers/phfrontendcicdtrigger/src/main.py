import os
import json
import boto3
import datetime
import math
import traceback
'''
event = {
    "version": "Current",
    "publisher": "hbzhao",
    "runtime": "dev",
    "trigger": {
        "branch": "PBDP-3235-cicd",
        "commit": "184d0599303ccaa537417610c0dd6b929fe3a8a5",
        "repo": "micro-frontend",
        "components": [
            {
                "prefix": "client-helper/offweb-model-helper"
            }
        ],
        "required": true
    }
}
'''

def lambda_handler(event, context):
    # 1503
    event = json.loads(event["body"])
    print(event)

    execution_time = str(math.floor(datetime.datetime.now().timestamp() * 1000))
    state_machine_event = {
        "common": {
            "version": event["version"],
            "publisher": event["publisher"],
            "runtime": event["runtime"],
            "email": event["email"],
            "invalidate": event["invalidate"],
            "executionName": execution_time
        },
        "frontend": {
            "required": False
        }
    }
    if event.get("frontend"):
        frontend = {
            "repo": event["frontend"]["repo"],
            "branch": event["frontend"]["branch"],
            "commit": event["frontend"]["commit"],
            "components": event["frontend"]["components"],
            "required": event["frontend"]["required"]
        }
        state_machine_event["frontend"] = frontend

    state_machine_arn = "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:frontendcicd"
    client = boto3.client('stepfunctions')
    res = client.start_execution(stateMachineArn=state_machine_arn,
                                 input=json.dumps(state_machine_event),
                                 name=execution_time)
    run_arn = res['executionArn']
    print("Started  ARN is %s.", run_arn)

    result = {
        "status": "ok",
        "message": "start run " + run_arn + " deploy components:" + ",".join([i["prefix"].split("/")[-1] for i in event["frontend"]["components"]])
    }
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(result)
    }
