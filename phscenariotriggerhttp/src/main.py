import os
import json
from triggerupdate import scenarioCUProcessor


def lambda_handler(event, context):
    event = json.loads(event["body"])
    print(event)

    tenantId = event.get('tenantId', 'pharbers')
    targetArn = event.get('targetArn', 'arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phscenariotriggerhandler-dev')
    projectId = event['project-id']
    scenarioId = event['scenario-id']
    triggerId = event['trigger-id']
    cronExpression = event.get('cron', '')
    
    result = scenarioCUProcessor(tenantId, targetArn, projectId, scenarioId, triggerId, cronExpression)
    
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(result)
    }