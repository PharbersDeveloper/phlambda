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


def get_ssm():
    ssm = boto3.client('ssm', region_name="cn-northwest-1")
    responses = ssm.describe_parameters().get("Parameters")
    return [response.get("name") for response in responses]


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
    traceId = event.get("common").get("traceId")
    # TODO: 缺判断当前这个是否已经启动 @ylzhang
    if traceId in get_ssm():
        pass

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

    # TODO: ... 在这里看是否能创建。这个地方也会是创建流程的唯一入口
    # 1. stack 是否存在，如果存在 报错，不能重复创建
    #     1.1 stackname 的获取方法是 在dynamodb中找到resource 表中 tenantid 下的所有 ownership 为 shared 值的 
    #     1.2 对每一个值中的property 遍历，形成一个stackname 的数组
    #     1.3 stackname 的名字规则为  <role>-<property.type>-<tenantId>
    #     1.4 所有的stak 在cloud formation 中都不存在 算过，要不然报错，说哪一个 stack 指向的role 以及type 存在
    #        
    # 2. ssm 是否存在，如果存在，报错，不能重复创建并提交管理员
    # @ylzhang


    try:
        trace_id = args["common"]["traceId"]
        # state_machine_arn = os.environ["ARN"]
        state_machine_arn = f"arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:tenant-boot"
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
