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
        "current": 0
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

    if len(response['Stacks']) > 0 and response['Stacks'][0]['StackStatus'] == event['CREATE_COMPLETE']:
        return event["current"] + 1
    else:
        return event["current"]
