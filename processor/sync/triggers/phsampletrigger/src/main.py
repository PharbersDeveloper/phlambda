import os
import json
import boto3
import traceback
from phmetriclayer import aws_cloudwatch_put_metric_data


def lambda_handler(event, context):
    # 1516
    event = json.loads(event["body"])
    calculate = event.get("calculate")
    print(event)

    projectId = event['common']['tenantId']
    dryRun = event.get('dryRun', False)

    ssm_client = boto3.client('ssm')
    response = ssm_client.get_parameter(
        Name=projectId,
    )
    value = json.loads(response["Parameter"]["Value"])

    event["Actions"] = {
            "cat": calculate.get("type"),
            "desc": "sample",
            "comments": "something need to say",
            "message": {"optionName": calculate.get("type"), "cat": calculate.get("datasetType"), "runtime": "", "actionName": calculate.get("datasetName")},
            "required": True
        }

    event['engine'] = {
        'type': 'awsemr',
        'id': value['engine']["ClusterID"],
        'dss': {
            "ip": value["olap"]["PrivateIp"]
        }
    }

    print(event)
    if not dryRun:
        state_machine_arn = os.environ["ARN"]
        edition = "-" + os.getenv("EDITION")
        run_name = event['common']['runnerId'].replace("_", "-").replace(":", "-").replace("+", "-")
        client = boto3.client('stepfunctions')
        res = client.start_execution(stateMachineArn=state_machine_arn + edition, name=run_name, input=json.dumps(event))
        run_arn = res['executionArn']
        print("Started run %s. ARN is %s.", run_name, run_arn)

    # try:
    #     client = boto3.client('stepfunctions')
    #     res = client.start_execution(stateMachineArn=state_machine_arn, name=run_name, input=json.dumps(event))
    #     run_arn = res['executionArn']
    #     print("Started run %s. ARN is %s.", run_name, run_arn)
    # except Exception:
    #     print("Couldn't start run %s.", run_name)
    #     traceback.print_stack()
    #     error = {
    #         "status": "failed",
    #         "message": "Couldn't start run " + run_name
    #     }
    #     return {
    #         "statusCode": 200,
    #         "headers": {
    #             "Access-Control-Allow-Headers": "Content-Type",
    #             "Access-Control-Allow-Origin": "*",
    #             "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
    #         },
    #         "body": json.dumps(error)
    #     }

    result = {
        "status": "ok",
        "message": "start run " + run_name
    }

    #---------------------- ?????? -------------------------------------#
    aws_cloudwatch_put_metric_data(NameSpace='pharbers-platform',
                                   MetricName='platform-usage',
                                   tenantId=event["common"]["tenantId"])
    #---------------------- ?????? -------------------------------------#

    return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
            },
            "body": json.dumps(result)
        }
