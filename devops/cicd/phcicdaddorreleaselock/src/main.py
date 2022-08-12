import os
import json
import boto3

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
ssm_client = boto3.client('ssm')
'''
将错误提取出来写入到notification中
args:
    event = {
                "projectId": "ggjpDje20HUC2JW",
                "traceId": "",
                "projectName": "demo",
                "owner": "alfred",
                "showName": "alfred",
                "errors": {
                }
            },
return:
    {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": errors
    }
}
'''
def get_dict_ssm_parameter(parameter_name):

    try:
        response = ssm_client.get_parameter(
            Name=parameter_name,
        )
        value = json.loads(response["Parameter"]["Value"])
    except ssm_client.exceptions.ParameterNotFound as e:
        print("参数不存在")
        value = {}
    except Exception as e:
        raise e
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


def delete_ssm_parameter(parameter_name):
    ssm_client.delete_parameter(
        Name=parameter_name
    )

    return parameter_name


def lambda_handler(event, context):
    print(event)
    # 判断
    # type add/release
    whether_continue = False
    # 判断是否上锁
    if event["lockType"] == "add":
        if not get_dict_ssm_parameter(event["stateMachineName"] + "-lock"):
            # 没有上锁则加锁
            put_dict_ssm_parameter(event["stateMachineName"] + "-lock", "lock")
            whether_continue = True
        else:
            raise Exception("state machine is deploying")
    if event["lockType"] == "release":
        delete_ssm_parameter(event["stateMachineName"] + "-lock")
        whether_continue = True
    return {
        "continue": whether_continue
    }
