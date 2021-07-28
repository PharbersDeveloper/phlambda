import json
import boto3


def lambda_handler(event, context):
    # 测试cicd3
    body = json.loads(event['body'])
    step_client = boto3.client("stepfunctions")
    executionArn = body['executionArn']

    # 获取执行状态
    response = step_client.describe_execution(
        executionArn=executionArn
    )
    execution_status = response['status']

    last_enter_event = {}
    last_exited_event = {}
    enter_steps = []
    exited_steps = []

    if not execution_status == "SUCCEEDED":
        # 获取执行的历史
        response = step_client.get_execution_history(
            executionArn=executionArn,
            maxResults=333,
            includeExecutionData=False
        )

        # 如果是COMPLETE 不获取异常的step

        # 获取所有Enter的step
        for event in response['events']:
            index_event = response['events'].index(event)
            response['events'][index_event]["timestamp"] = "time"
            for key in response['events'][index_event].keys():
                if "Entered" in key:
                    last_enter_event = response['events'][index_event][key]
                    enter_steps.append(last_enter_event['name'])
        # 获取所有Exit的step
        for event in response['events']:
            index_event = response['events'].index(event)
            response['events'][index_event]["timestamp"] = "time"
            for key in response['events'][index_event].keys():
                if "Exited" in key:
                    last_exited_event = response['events'][index_event][key]
                    exited_steps.append(last_exited_event['name'])
        # 获取所有Enter 但没有Exit的step
        for exited_step in exited_steps:
            if exited_step in enter_steps:
                enter_steps.remove(exited_step)

    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
        },
        'body': json.dumps({
            "execution_status": execution_status,
            "steps": enter_steps
        })
    }

