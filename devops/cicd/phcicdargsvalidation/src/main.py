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
        value = response["Parameter"]["Value"]
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


def judge_runtime(runtime):
    runtime_list = get_dict_ssm_parameter("runtime")
    if runtime not in runtime_list:
        raise Exception("this runtime is invalid runtime")


def lambda_handler(event, context):
    print(event)
    judge_runtime(event["common"]["runtime"])
    # 判断本次deploy的version是否正确
    # 普通用户不能发布release版本 release对应的version其他runtime不能发布
    release_version = get_dict_ssm_parameter("release_version")
    dev_version = get_dict_ssm_parameter("dev_version")
    # 如果不是release 判断version是不是与ssm中release的version相同
    if event["common"]["runtime"] == "dev" and event["common"]["version"] == release_version:
        raise Exception("this version is release version")
    if event["common"]["runtime"] == "test" and event["common"]["version"] == release_version or dev_version:
        raise Exception("this version is invalid version")

    # 判断runtime是不是release
    if event["common"]["runtime"] == "release" and event["common"]["version"] != release_version:
        # 如果是release 判断version是否与ssm中相同 不同的话则更新
        put_dict_ssm_parameter("release_version", event["common"]["version"])
    if event["common"]["runtime"] == "dev" and event["common"]["version"] != dev_version:
        # 如果是release 判断version是否与ssm中相同 不同的话则更新
        put_dict_ssm_parameter("dev_version", event["common"]["version"])

    return 1