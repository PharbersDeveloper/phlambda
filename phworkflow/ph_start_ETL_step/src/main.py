import json
import boto3
from snowflakeId import snowflake

def lambda_handler(event, context):
    machine_input = {}

    ssm_client = boto3.client('ssm')
    ssm_response = ssm_client.get_parameter(
        Name='cluster_id'
    )

    len_parameters = len(event['parameters'])
    iterator = {
        "count": len_parameters + 1,
        "index": 0,
        "step": 1
    }

    machine_input['clusterId'] = ssm_response['Parameter']['Value']
    machine_input['iterator'] = iterator
    machine_input['parameters'] = event['parameters']

    snowflake_id = snowflake.IdWorker(1, 2, 0)
    execution_name = event['executor'] + "_" + str(snowflake_id.get_id())

    step_client = boto3.client('stepfunctions')
    # 启动状态机
    start_response = step_client.start_execution(
        stateMachineArn='arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:ETL_Iterator',
        name=execution_name,
        input=json.dumps(machine_input)
    )

    return start_response['executionArn']