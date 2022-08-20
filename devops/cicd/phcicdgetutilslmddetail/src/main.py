import json
import boto3
ssm_client = boto3.client('ssm')
'''
处理lmd和api相关信息
args:
    event = {
        "version": "0-0-1",
        "publisher": "赵浩博",
        "alias": "0-0-1",
        "runtime": "dev",
        "utils": {
            "commit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
            "repo": "phlambda",
            "branch": "feature/PBDP-3043-async-cicd-state-machine",
            "prefix": "processor/utils",
            "functionName": "cfnlambda",
            "required": true
        }
return:
    {   
        "lambdaArgs": {
            "name": "cfnlambdacodebuild",
            "cfn": "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cicd/template/phlambda-codebuild.yaml",
            "parameters": {
              "FunctionName": "cfnlambda",
              "BuildSpec": "lmdAndApiBuildspec",
              "FunctionPath": "processor/utils/cfnlambda",
              "FunctionPathPrefix": "processor/utils",
              "GitCommit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
              "GitUrl": "http://hbzhao:123456@192.168.53.179:7990/scm/lgc/phlambda.git",
              "BranchName": "feature/PBDP-3043-async-cicd-state-machine",
              "RepoName": "phlambda",
              "Version": "0-0-1"
            },
    }
'''
codebuild_cfn_path = "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cicd/template/phlambda-codebuild.yaml"
git_url = "http://cicd:Abcde196125@192.168.53.179:7990/scm/lgc/phlambda.git"
buildSpec = "lmdUtilsBuildspec"


def get_dict_ssm_parameter(parameter_name):

    response = ssm_client.get_parameter(
        Name=parameter_name,
    )
    value = json.loads(response["Parameter"]["Value"])

    return value


def create_lmd_args(event):
    lmd_args = {
        "name": event["utils"]["functionName"] + "codebuild",
        "cfn": codebuild_cfn_path,
        "parameters": {
            "FunctionName": event["utils"]["functionName"],
            "BuildSpec": buildSpec,
            "FunctionPath": event["utils"]["prefix"] + "/" + event["utils"]["functionName"],
            "FunctionPathPrefix": event["utils"]["prefix"],
            "GitCommit": event["utils"]["commit"],
            "GitUrl": git_url,
            "BranchName": event["utils"]["branch"],
            "RepoName": event["utils"]["repo"],
            "Version": event["version"]
        }
    }
    return lmd_args


def lambda_handler(event, context):
    print(event)
    # 1 处理lmd相关信息 返回lambdaArgs 参数用于运行codebuild
    lmd_args = create_lmd_args(event)
    # 2 处理apiGateway相关信息 返回apiGateWayArgs
    # RestApiId AuthorizerId ParentId 根据runtime进行获取
    iterator = {
        "index": 0,
        "currentStatus": "running"
    }
    lmdCounts = 1
    stackName = event["utils"]["functionName"] + "-utilsresource"

    return {
        "lmdCounts": lmdCounts,
        "iterator": iterator,
        "lambdaArgs": lmd_args,
        "stackName": stackName
    }
