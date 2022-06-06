import os
import json
import boto3
import traceback
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    event = json.loads(event["body"])
    print(event)
    # "resourceId": "mIMzFAKEyU6JBc7nl1NmBA==",
    result = {
        "status": "",
        "message": "",
        "trace_id": "",
        "resourceId": "",
    }
    # trace_id = ""
    # edition = "" if os.getenv("EDITION") == "V2" else "-dev"
    # traceId = event.get("common").get("traceId")

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
            "cat": "personalres-boot",
            "desc": "reboot project",
            "comments": "something need to say",
            "message": "something need to say",
            "required": True
        },
        "resourcesId": "resourceId",  # TODO: 从 event 中找到 resourceID @mzhang
        "notification": {
            "required": True
        }   
    }

    # TODO: ... 在这里看是否能创建。这个地方也会是创建流程的唯一入口

    # 1. stack 是否存在，如果存在 报错，不能重复创建
    #     1.1 stackname 的获取方法是 在dynamodb中找到resource 根据resource id 找到需要创建的项
    #     1.2 对每一个值中的property 遍历，形成一个stackname 的数组
    #     1.3 stackname 的名字规则为  <role>-<property.type>-<tenantId>-<ownership>-<owner>
    #     1.4 所有的stak 在cloud formation 中都不存在 算过，要不然报错，说哪一个 stack 指向的role 以及type 存在
    # 2. ssm 是否存在，如果存在，报错，不能重复创建并提交管理员
    # @mzhang

    try:
        trace_id = args["common"]["traceId"]
        # state_machine_arn = os.environ["ARN"]
        state_machine_arn = f"arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:personal-res-boot"
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
        result["message"] = "Couldn't start run " + trace_id
        result["trace_id"] = trace_id

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(result)
    }
