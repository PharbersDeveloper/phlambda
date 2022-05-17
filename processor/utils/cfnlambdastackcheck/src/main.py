import os
import json
import boto3
import traceback
import datetime

client = boto3.client('cloudformation')

'''
# cloud formation stack 创建与删除

args:
    event = {
        "current": {
            "index": 0,
            "currentStatus": ""
        }
        "name": "",
        "expect": "CREATE_COMPLETE"

    }

return:
    {
        
    }
'''


def lambda_handler(event, context):
    print(event)

    stackName = event["name"].replace("_", "-").replace(":", "-").replace("+", "-")

    response = client.describe_stacks(
        StackName=stackName #  event['runnerId']
    )
    print(response)

    # TODO: 当有失败的情况
    if len(response['Stacks']) > 0 and response['Stacks'][0]['StackStatus'] == event['expect']:
        return {
            "index": event["current"] + 1,
            "currentStatus": "success"
        }
    elif len(response['Stacks']) > 0 and response['Stacks'][0]['StackStatus'] == "ROLLBACK_COMPLETE":
        raise Exception('create ' + name + ' failed')
    else:
        return {
            "index": event["current"],
            "currentStatus": "running"
        }
