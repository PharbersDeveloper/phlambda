import os
import json
import boto3
import traceback


'''
args =
{
    "common": {
        "tenantId": "zudIcG_17yj8CEUoCTHg",
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "projectStart",
        "desc": "reboot project",
        "comments": "something need to say",
        "message": "something need to say",
        "required": true
    },
    "resources": [
        "emr", "chlickhouse", "chproxy"
    ],
    "notification": {
        "required": true
    }
}

event = {
    tenantId: "String",
    traceId: "String",
    owner: "String",
    showName: "String"
}
'''

def lambda_handler(event, context):
    event = json.loads(event["body"])
    print(event)
    result = {
        "status": "",
        "message": "",
        "trace_id": ""
    }
    trace_id = ""
    edition = "" if os.getenv("EDITION") == "V2" else "-dev"

    # TODO: 缺判断当前这个是否已经启动 @ylzhang

    # 1. event to args
    args = {
        "common": {
            "tenantId": event["tenantId"],
            "traceId": event["traceId"],
            "projectId": "ggjpDje0HUC2JW",
            "projectName": "demo",
            "owner": event["owner"],
            "showName": event["showName"]
        },
        "action": {
            "cat": "tenant-boot",
            "desc": "reboot project",
            "comments": "something need to say",
            "message": "something need to say",
            "required": True
        },
        "resources": [
            "emr", "chlickhouse", "chproxy"
        ],
        "notification": {
            "required": True
        }   
    }

    try:
        trace_id = args["common"]["traceId"]
        # state_machine_arn = os.environ["ARN"]
        state_machine_arn = f"arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:tenant-termination"
        client = boto3.client("stepfunctions")
        res = client.start_execution(stateMachineArn=state_machine_arn + edition,
                                     name=trace_id, input=json.dumps(args, ensure_ascii=False))
        run_arn = res["executionArn"]
        print("Started run %s. ARN is %s.", trace_id, run_arn)
        result["status"] = "succeed"
        result["message"] = "start run " + trace_id
        result["trace_id"] = trace_id

    except Exception:
        result["status"] = "failed"
        result["message"] = "succeed"
        result["trace_id"] = "Couldn't start run " + trace_id

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(result)
    }
