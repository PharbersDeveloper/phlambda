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


def download_s3_file(bucket, key, file_path):
    s3_resource.meta.client.download_file(
        Bucket=bucket,
        Key=key,
        Filename=file_path
    )


def upload_s3_file(bucket, key, file_path):
    s3_client.upload_file(
        Bucket=bucket,
        Key=key,
        Filename=file_path
    )


def replace_file(resource, target):
    print(f"sed -i s#{resource}\"#{target}\"# '/tmp/sm.json'")
    os.system(f"sed -i s#{resource}\\\"#{target}\\\"# '/tmp/sm.json'")


def lambda_handler(event, context):
    print(event)
    # 判断当前 smName + runtime + "-resource" 是否在SSM中存在
    ssm_name = event["stateMachineName"] #+ "-" + event["runtime"] + "-resource"
    sm_args = get_dict_ssm_parameter(ssm_name)
    sm_value = sm_args.get(event["runtime"], {})
    # 如果不存在则进行创建 存在则更新里面lmd 的信息
    # 更新本次发布中lmd的version
    for lambdaArg in event["lambdaArgs"]:
        sm_value[lambdaArg["functionName"]] = lambdaArg["version"]
    sm_args[event["runtime"]] = sm_value
    print(sm_args)
    put_dict_ssm_parameter(ssm_name, json.dumps(sm_args))

    # 下载sm.json
    download_s3_file(event["smJsonPathBucket"], event["smJsonPathKey"], "/tmp/sm.json")

    # 修改sm.json的内容
    for lmd, version in sm_value.items():
        replace_file(lmd, lmd + ":" + version)

    stateMachines = get_dict_ssm_parameter("statemachine")
    for statemachine in stateMachines:
        replace_file(statemachine, statemachine + "-" + event["runtime"])

    # 上传sm.json
    upload_s3_file(event["smJsonPathBucket"], event["smJsonPathKey"].replace("sm.json", "modify_sm.json"), "/tmp/sm.json")
    return 1
