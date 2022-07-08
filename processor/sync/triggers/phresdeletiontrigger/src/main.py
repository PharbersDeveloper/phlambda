import os
import json
import boto3
from phmetriclayer import aws_cloudwatch_put_metric_data

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
        res = client.start_execution(stateMachineArn=state_machine_arn + edition,
                                     name=trace_id, input=json.dumps(event, ensure_ascii=False))
        run_arn = res["executionArn"]
        print("Started run %s. ARN is %s.", trace_id, run_arn)
        result["status"] = "succeed"
        result["message"] = "start run " + trace_id
        result["trace_id"] = trace_id

    except Exception:
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
