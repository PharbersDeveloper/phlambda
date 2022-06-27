import os
import json
import boto3
import traceback


def lambda_handler(event, context):
    # 1516
    event = json.loads(event["body"])
    print(event)

    projectId = event['common']['tenantId']
    dryRun = event.get('dryRun', False)

    ssm_client = boto3.client('ssm')
    response = ssm_client.get_parameter(
        Name=projectId,
    )
    value = json.loads(response["Parameter"]["Value"])

    event['engine'] = {
        'type': 'awsemr',
        'id': value['engine']["ClusterID"],
        'dss': {
            "ip": value["olap"]["PrivateIp"]
        }
    }

    print(event)
    if not dryRun:
        state_machine_arn = f"arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:pharbers-trigger-dev"
        run_name = event['common']['runnerId'].replace("_", "-").replace(":", "-").replace("+", "-")
        client = boto3.client('stepfunctions')
        res = client.start_execution(stateMachineArn=state_machine_arn, name=run_name, input=json.dumps(event))
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
    return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
            },
            "body": json.dumps(result)
        }
