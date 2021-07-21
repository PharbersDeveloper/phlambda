import json
import boto3
from src.snowflakeId import snowflake

def lambda_handler(event, context):

    body = json.loads(event['body'])
    machine_input = {}
    executor = "executor"
    parameters = body['parameters']

    ssm_client = boto3.client('ssm')
    ssm_response = ssm_client.get_parameter(
        Name='cluster_id'
    )

    len_parameters = len(parameters)
    iterator = {
        "count": len_parameters + 1,
        "index": 0,
        "step": 1
    }

    machine_input['clusterId'] = ssm_response['Parameter']['Value']
    machine_input['iterator'] = iterator
    machine_input['parameters'] = parameters

    snowflake_id = snowflake.IdWorker(1, 2, 0)
    execution_name = executor + "_" + str(snowflake_id.get_id())

    step_client = boto3.client('stepfunctions')
    # 启动状态机
    start_response = step_client.start_execution(
        stateMachineArn='arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:ETL_Iterator',
        name=execution_name,
        input=json.dumps(machine_input)
    )
    executionArn = start_response['executionArn']

    return {
        'statusCode': 200,
        'body': json.dumps({
            "executionArn": executionArn
        })
    }