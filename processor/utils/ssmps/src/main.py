import os
import json
import boto3
import traceback
import datetime

ssm_client = boto3.client('ssm')
'''
# ssm parameter store 的读写

args:
    event = {
        "action": "read | write", 
        "key": "String",
        "value": {
            ...
        }
    }

return:
    {
        
    }
'''


def get_dict_ssm_parameter(parameter_name):

    response = ssm_client.get_parameter(
        Name=parameter_name,
    )
    value = json.loads(response["Parameter"]["Value"])

    return value


def lambda_handler(event, context):
    print(event)
    # 通过key 从ssm获取resource
    resources = get_dict_ssm_parameter(event["key"])

    return resources
