import os
import json
import boto3
from phmetriclayer import aws_cloudwatch_put_metric_data

# {
#   "common": {
#     "traceId": "1ecf64ce0a7441cc9db9f118f93gb423",
#     "tenantId": "zudIcG_17yj8CEUoCTHg",
#     "projectId": "3YDabKO2IFh6eJJ",
#     "projectName": "header",
#     "owner": "alfred",
#     "showName": "alfred"
#   },
#   "action": {
#     "cat": "tenantStop",
#     "desc": "terminate project",
#     "comments": "something need to say",
#     "message": "something need to say",
#     "required": true
#   },
#   "resources": {"traceId": "alfred-resource-creation-traceId",
#                 "engine": {"ClusterID": "j-PX68RDFOX82D",
#                            "ClusterDNS": "ec2-52-82-68-6.cn-northwest-1.compute.amazonaws.com.cn"},
#                 "olap": {"PrivateIp": "192.168.55.39",
#                          "PublicIp": "69.230.248.188",
#                          "PrivateDns": "ip-192-168-55-39.cn-northwest-1.compute.internal",
#                          "PublicDns": "ec2-69-230-248-188.cn-northwest-1.compute.amazonaws.com.cn"}
#                 },
#   "notification": {
#     "required": true
#   }
# }


def lambda_handler(event, context):
    event = json.loads(event["body"])
    print(event)

    result = {
        "status": "",
        "message": "",
        "trace_id": ""
    }
    trace_id = ""
    edition = "-dev" #if os.getenv("EDITION") == "V2" else "-dev"
    try:
        trace_id = event["common"]["traceId"]
        state_machine_arn = os.environ["ARN"]
        client = boto3.client("stepfunctions")
        res = client.start_execution(stateMachineArn=state_machine_arn,#+ edition,
                                     name=trace_id, input=json.dumps(event, ensure_ascii=False))
        run_arn = res["executionArn"]
        print("Started run %s. ARN is %s.", trace_id, run_arn)
        result["status"] = "succeed"
        result["message"] = "start run " + trace_id
        result["trace_id"] = trace_id

    except Exception as e:
        print("*"*50 + "ERROR" + "*"*50 + "\n", str(e))
        result["status"] = "failed"
        result["message"] = "succeed"
        result["trace_id"] = "Couldn't start run " + trace_id

    #---------------------- 埋点 -------------------------------------#
    aws_cloudwatch_put_metric_data(NameSpace='pharbers-platform',
                                   MetricName='platform-usage',
                                   tenantId=event["common"]["tenantId"])
    #---------------------- 埋点 -------------------------------------#


    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(result)
    }
