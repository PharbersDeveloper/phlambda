import os
import json
import boto3
import traceback
from boto3.dynamodb.conditions import Key


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
        "emr", "clickhouse", "chproxy"
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


ssm = boto3.client('ssm')
cloudformation = boto3.client('cloudformation')
dynamodb = boto3.resource("dynamodb")


def check_cloudformation_stack(StackName):
    try:
        response = cloudformation.describe_stacks(
            StackName=StackName,
        )
        return True
    except:
        pass


def check_ssm(stack_name):
    try:
        response = ssm.get_parameter(
            Name=stack_name
        )
        return True
    except:
        pass


def query_resource(tenantId):
    table = dynamodb.Table("resource")
    response = table.query(
        KeyConditionExpression=Key('tenantId').eq(tenantId),
    )
    return response.get("Items")


def get_stack_name(tenantId):
    resource_item = query_resource(tenantId)
    item_list = [item for item in resource_item if item.get("ownership") == "shared"]

    res_list = []
    for item in item_list:
        res_list += [f'{item.get("role")}-{property.get("type")}-{tenantId.replace("_", "-").replace(":", "-").replace("+", "-")}' for property in
                     json.loads(item.get("properties"))]
    return res_list



def lambda_handler(event, context):
    event = json.loads(event["body"])
    print(event)
    result = {
        "status": "",
        "message": "",
        "trace_id": ""
    }
    trace_id = ""
    edition = "-" + os.getenv("EDITION")
    # TODO: ... ??????????????????????????????????????? @ylzhang

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
            "cat": "tenantStop",
            "desc": "reboot project",
            "comments": "",
            "message": {"optionName": "tenant_stop", "cat": "", "runtime": "", "actionName": ""},
            "required": True
        },
        "resources": [
            "emr", "clickhouse", "chproxy"
        ],
        "notification": {
            "required": True
        }   
    }

    ssm_message = []
    cloudformation_message = []
    tenantId = args.get("common").get("tenantId")
    stack_list = get_stack_name(tenantId)
    for stack_name in stack_list:
        if check_cloudformation_stack(stack_name):
            cloudformation_message.append(f"tenantId: {tenantId} role: {stack_name.split('-')[0]} type: {stack_name.split('-')[1]}.")
        if check_ssm(event["tenantId"]):
            ssm_message.append(f"tenantId: {tenantId} role: {stack_name.split('-')[0]} type: {stack_name.split('-')[1]}.")

    if not ssm_message or not cloudformation_message:
        result["status"] = "failed"
        result["message"] = json.dumps({"stackName not exits": {"ssm": ssm_message, "cloudformation": cloudformation_message}})
        result["trace_id"] = args["common"]["traceId"]
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
            },
            "body": json.dumps(result)
        }

    try:
        trace_id = args["common"]["traceId"]
        state_machine_arn = os.environ["ARN"]
        # state_machine_arn = f"arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:tenantstop"
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
