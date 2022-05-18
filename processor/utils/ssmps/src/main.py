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
        "action": "read | write | delete", 
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


def put_dict_ssm_parameter(parameter_name, parameter_value):

    response = ssm_client.put_parameter(
        Name=parameter_name,
        Value=parameter_value,
        Type="String",
        Overwrite=True
    )

    print(response)
    return parameter_value


def delete_dict_ssm_parameter(parameter_name):

    response = ssm_client.delete_parameter(
        Name=parameter_name,
    )
    print(response)


def lambda_handler(event, context):
    print(event)
    # 通过key 从ssm获取resource
    resources = True
    if event["action"] == "read":
        resources = get_dict_ssm_parameter(event["key"])
    elif event["action"] == "write":
        put_dict_ssm_parameter(event["key"], json.dumps(event["value"]))
        resources = event["value"]
    elif event["action"] == "delete":
        delete_dict_ssm_parameter(event["key"])

    return resources
