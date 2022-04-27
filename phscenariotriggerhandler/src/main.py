import os
import json
import boto3
import traceback
from datetime import datetime
from boto3.dynamodb.conditions import Key


def triggerExecution(projectId, scenarioId, step, dynamodb):
    
    # debug
    dryRun = True

    # 2. 读scenario中的详细信息，projectName
    scenario_table = dynamodb.Table('scenario')
    scenario = scenario_table.query(
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("id").eq(scenarioId)
    )['Items'][0]
    projectName = scenario['projectName']
    
    # 3. runerId
    dt = datetime.now()
    d = dt.isoformat()
    i = d.index(".")
    d = d[0:i] + "+00:00"
    runnerId = "_".join([projectName, projectName, 'developer', d])
    print(runnerId)

    # 4. step detail
    stepDetial = json.loads(step['detail'])
    print(stepDetial)
    dsName = stepDetial['name']
    recursive = stepDetial['recursive']

    # 0. create event
    event = {
        'common': {
            'runnerId': runnerId,
            'projectId': projectId,
            'projectName': projectName,
            'owner': scenario.get('owner', 'scenario'),
            'showName': scenario.get('owner', 'scenario'),
        },
        'calculate': {
            'type': 'dataset',
            'name': dsName,
            'conf': '',
            'recursive': True
        },
        'dryRun': dryRun,
        'recursive': recursive
    }

    # 1. ssm
    ssm_client = boto3.client('ssm')
    response = ssm_client.get_parameter(
        Name=projectId,
    )
    value = json.loads(response["Parameter"]["Value"])

    event['engine'] = {
        'type': 'awsemr',
        'id': value['clusters'][0]['id'],
        'dss': {
            "ip": value.get("proxies")[0]
        }
    }

    print(event)

    run_name = ''
    if not dryRun:
        state_machine_arn = 'arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:pharbers-trigger'
        run_name = event['common']['runnerId'].replace("_", "-").replace(":", "-").replace("+", "-")
        client = boto3.client('stepfunctions')
        res = client.start_execution(stateMachineArn=state_machine_arn, name=run_name, input=json.dumps(event))
        run_arn = res['executionArn']
        print("Started run %s. ARN is %s.", run_name, run_arn)
    else:
        run_name = "dryRun"
    
    result = {
        "status": "ok",
        "message": "start run " + run_name
    }
    return result


def lambda_handler(event, context):
    print(event)

    scenarioId = event['ScenarioId']
    projectId = event['ProjectId']
    TriggerId = event['TriggerId']

    scenarioKey = ('_').join([projectId, scenarioId])


    # 0. 测试阶段
    isDebug = True

    # 1. 从数据库中读step的详细描述
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('scenario_step')
    items = table.query(
        Select='ALL_ATTRIBUTES',
        Limit=1000,
        ExpressionAttributeValues={
            ':v1': scenarioKey
        },
        KeyConditionExpression='scenarioId=:v1'
    )['Items']
    print(items)

    if len(items) == 0:
        print('no need to trigger anything')
        result['status'] = 'error'
        result['message'] = 'no need to trigger anything'
    else:
        if len(items) > 1:
            print('only to trigger the first step')    

        step = items[0]
        result = triggerExecution(projectId, scenarioId, step, dynamodb)
    
    return result