import json
import boto3
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
cfn_client = boto3.client('cloudformation')
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


def delete_ssm_parameter(parameter_name):
    ssm_client.delete_parameter(
        Name=parameter_name
    )

    return parameter_name


def get_stack_status(stackName):
    result = False
    faliedStatus = ["UPDATE_ROLLBACK_COMPLETE"]
    response = cfn_client.describe_stacks(
        StackName=stackName
    )
    if response['Stacks'][0]['StackStatus'] in faliedStatus and len(response['Stacks']) > 0:
        result = True
    return result


def copy_manage_resource(bucket_name, prefix):
    copy_source = {
        'Bucket': bucket_name,
        'Key': prefix + "/manage_back.yaml"
    }
    s3_resource.meta.client.copy(copy_source, bucket_name, prefix + "/manage.yaml")


def del_s3_resource(bucket, key):
    response = s3_client.delete_object(
        Bucket=bucket,
        Key=key
    )


def judge_stack_exist(stackName):
    stack_exist = False
    try:
        response = cfn_client.describe_stacks(
            StackName=stackName
        )
        stack_exist = True
        print(response)
    except Exception as e:
        print(e)
    return stack_exist


def delete_stack(stackName):
    response = cfn_client.delete_stack(
        StackName=stackName
    )


def lambda_handler(event, context):
    print(event)
    # 如果创建失败 则删除cloudformation 同时删除s3上cicd/prefix/manage.yaml
    # 判断processor 和trigger 里面的required是否为true
    # 需要判断是codebuild 错误还是update yaml 错误
    # 根据manage back yaml是否存在
    if event["processor"]["required"]:
        lock_name = event["processor"]["stateMachineName"] + "-resource" + "-lock"
        if get_dict_ssm_parameter(lock_name):
            delete_ssm_parameter(lock_name)
        del_s3_resource("ph-platform", "2020-11-11/cicd/" + event["processor"]["prefix"] + "/manage.yaml")
        # 判断这次操作是不是update操作
        if get_stack_status(event["processor"]["stateMachineName"] + "-resource") and judge_stack_exist(event["processor"]["stateMachineName"] + "-resource"):
            # 如果update失败 将cicd/prefix/manage_back.yaml 文件恢复到manage.yaml文件
            copy_manage_resource("ph-platform", "2020-11-11/cicd/" + event["processor"]["prefix"])
            # del_s3_resource("ph-platform", "2020-11-11/cicd/" + event["processor"]["prefix"] + "/manage_back.yaml")
        for function in event["processor"]["functions"]:
            if judge_stack_exist(function["name"] + "codebuild"):
                delete_stack(function["name"] + "codebuild")

    if event["trigger"]["required"]:
        del_s3_resource("ph-platform", "2020-11-11/cicd/" + event["trigger"]["prefix"] + event["trigger"]["functionName"] + "/manage.yaml")
        # 判断这次操作是不是update操作
        functionName = event["trigger"]["functionName"]
        lock_name = functionName + "-apiresource" + "-lock"
        if get_dict_ssm_parameter(lock_name):
            delete_ssm_parameter(lock_name)
        if get_stack_status(functionName + "-apiresource") and judge_stack_exist(functionName + "-apiresource"):
            # 如果update失败 将cicd/prefix/manage_back.yaml 文件恢复到manage.yaml文件 删除manage_back文件
            copy_manage_resource("ph-platform", "2020-11-11/cicd/" + event["trigger"]["prefix"] + functionName )
            # del_s3_resource("ph-platform", "2020-11-11/cicd/" + event["trigger"]["prefix"] + "/manage_back.yaml")
        if judge_stack_exist(event["trigger"]["functionName"] + "codebuild"):
            delete_stack(event["trigger"]["functionName"] + "codebuild")

    if event["utils"]["required"]:
        del_s3_resource("ph-platform", "2020-11-11/cicd/" + event["utils"]["prefix"] + event["utils"]["functionName"] + "/manage.yaml")
        # 判断这次操作是不是update操作
        functionName = event["utils"]["functionName"]
        lock_name = functionName + "-utilsresource" + "-lock"
        if get_dict_ssm_parameter(lock_name):
            delete_ssm_parameter(lock_name)
        if get_stack_status(functionName + "-utilsresource") and judge_stack_exist(functionName + "-utilsresource"):
            # 如果update失败 将cicd/prefix/manage_back.yaml 文件恢复到manage.yaml文件 删除manage_back文件
            copy_manage_resource("ph-platform", "2020-11-11/cicd/" + event["utils"]["prefix"] + functionName)
            # del_s3_resource("ph-platform", "2020-11-11/cicd/" + event["trigger"]["prefix"] + "/manage_back.yaml")
        if judge_stack_exist(event["utils"]["functionName"] + "codebuild"):
            delete_stack(event["utils"]["functionName"] + "codebuild")

    if event["multistage"]["required"]:
        del_s3_resource("ph-platform", "2020-11-11/cicd/" + event["multistage"]["prefix"] + event["multistage"]["functionName"] + "/manage.yaml")
        # 判断这次操作是不是update操作
        functionName = event["multistage"]["functionName"]
        lock_name = functionName + "-apiresource" + "-lock"
        if get_dict_ssm_parameter(lock_name):
            delete_ssm_parameter(lock_name)
        if get_stack_status(functionName + "-apiresource") and judge_stack_exist(functionName + "-apiresource"):
            # 如果update失败 将cicd/prefix/manage_back.yaml 文件恢复到manage.yaml文件 删除manage_back文件
            copy_manage_resource("ph-platform", "2020-11-11/cicd/" + event["multistage"]["prefix"] + functionName)
            # del_s3_resource("ph-platform", "2020-11-11/cicd/" + event["trigger"]["prefix"] + "/manage_back.yaml")
        if judge_stack_exist(event["multistage"]["functionName"] + "codebuild"):
            delete_stack(event["multistage"]["functionName"] + "codebuild")

    return 1
