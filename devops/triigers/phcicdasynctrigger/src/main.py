import os
import json
import boto3
import traceback
'''
event = {
    "version": "Current",
    "publisher": "hbzhao",
    "runtime": "dev",
    "trigger": {
        "commit": "c8008002b1c34eb134b0bb893ab5fd7e43cc02da",
        "repo": "phlambda",
        "branch": "feature/PBDP-3043-async-cicd-state-machine",
        "prefix": "processor/sync/triggers/phnewsampletrigger",
        "entry": {
            "type": "ApiGateWay",
            "resource": "",
            "method": [
                "POST",
                "OPTIONS"
            ]
        },
        "required": true
    },
    "processor": {
        "repo": "phlambda",
        "branch": "feature/PBDP-3043-async-cicd-state-machine",
        "commit": "207d2c7173a434605ed7fa444c62c77b4a26eb78",
        "prefix": "processor/async/sample",
        "functions": [
            {
                "name": "phsampleclear"
            }
        ],
        "required": false
    }
}
'''

def lambda_handler(event, context):
    # 1503
    event = json.loads(event["body"])
    print(event)

    state_machine_event = {
        "common": {
            "version": event["version"],
            "publisher": event["publisher"],
            "alias": event["version"],
            "runtime": "dev" if event["version"] == "MINOR" else "v2"
        },
        "processor": {
            "repo": event["processor"]["repo"],
            "branch": event["processor"]["branch"],
            "commit": event["processor"]["commit"],
            "prefix": event["processor"]["prefix"],
            "stateMachineName": event["processor"]["prefix"].split("/")[-1],
            "sm": event["processor"]["prefix"] + "/sm.json",
            "functions": event["processor"]["functions"],
            "required": event["processor"]["required"]
        },
        "trigger": {
            "commit": event["trigger"]["commit"],
            "repo": event["trigger"]["repo"],
            "branch": event["trigger"]["branch"],
            "prefix": "/".join(event["trigger"]["prefix"].split("/")[0:-1]),
            "functionName": event["trigger"]["prefix"].split("/")[-1],
            "entry": event["trigger"]["entry"],
            "required": event["trigger"]["required"]
        }
    }

    state_machine_arn = "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:async-trigger-cicd"
    client = boto3.client('stepfunctions')
    res = client.start_execution(stateMachineArn=state_machine_arn, input=json.dumps(state_machine_event))
    run_arn = res['executionArn']
    print("Started  ARN is %s.", run_arn)
    result = {
        "status": "ok",
        "message": "start run " + run_arn
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
