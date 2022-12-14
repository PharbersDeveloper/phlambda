import json
import boto3
ssm_client = boto3.client('ssm')
'''
处理lmd和api相关信息
args:
    event = {
        "version": "V001",
        "publisher": "赵浩博",
        "alias": "V001",
        "runtime": "dev",
        "trigger": {
            "commit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
            "repo": "phlambda",
            "branch": "feature/PBDP-3043-async-cicd-state-machine",
            "prefix": "processor/sync/triggers",
            "functionName": "phsampletrigger",
            "auth": "oauth",              
            "entry": {
                "type": "Api GateWay",
                "resources": [
                    "offweb": {
                        "name": "offweb",
                        "methods": []
                    },
                    "offweb/{type}":{
                        "methods": ["GET","OPTIONS"]
                    },
                    "offweb/{type}/{id}":{
                        "methods": ["GET","OPTIONS"]
                    },
                    "offweb/{type}/{id}/relationships":{
                        "methods": ["OPTIONS"]
                    },
                    "offweb/{type}/{id}/relationships/{relationship}":{
                        "methods": ["GET","OPTIONS"]
                    },
                    "offweb/{type}/{id}/{relationship}":{
                        "methods": ["GET","OPTIONS"]
                    }
                }
            },
            "required": true
        }
return:
    {   
        "lambdaArgs": {
            "name": "phsampletriggercodebuild",
            "cfn": "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cicd/template/phlambda-codebuild.yaml",
            "parameters": {
              "FunctionName": "phsampletrigger",
              "BuildSpec": "lmdAndApiBuildspec",
              "FunctionPath": "processor/sync/triggers/phsampletrigger",
              "FunctionPathPrefix": "processor/sync/triggers",
              "GitCommit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
              "GitUrl": "http://hbzhao:123456@192.168.53.179:7990/scm/lgc/phlambda.git",
              "BranchName": "feature/PBDP-3043-async-cicd-state-machine",
              "RepoName": "phlambda",
              "Version": "V001"
            },
        "apiGateWayArgs": {
            "method": ["POST"],
            "PathPart": "phsampletrigger",
            "LmdName": "lmd-phsampletrigger-dev",
            "RestApiId": "",
            "AuthorizerId": "",
            "ParentId": ""
        }
    }
'''
nodejs_codebuild_cfn_path = "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cicd/template/phlambda-nodejs-codebuild.yaml"
codebuild_cfn_path = "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cicd/template/phlambda-codebuild.yaml"
git_url = "http://cicd:Abcde196125@192.168.53.179:7990/scm/lgc/phlambda.git"
buildSpec = "lmdAndApiBuildspec"
nodejsBuildSpec = "nodejsLmdAndApiBuildspec"


def get_dict_ssm_parameter(parameter_name):

    response = ssm_client.get_parameter(
        Name=parameter_name,
    )
    value = json.loads(response["Parameter"]["Value"])

    return value


def create_lmd_args(event):
    lmd_args = {
        "name": event["multistage"]["functionName"] + "codebuild",
        "cfn": codebuild_cfn_path,
        "parameters": {
            "FunctionName": event["multistage"]["functionName"],
            "BuildSpec": nodejsBuildSpec if event["multistage"]["functionRuntime"] == "nodejs" else buildSpec,
            "FunctionPath": event["multistage"]["prefix"] + "/" + event["multistage"]["functionName"],
            "FunctionPathPrefix": event["multistage"]["prefix"],
            "GitCommit": event["multistage"]["commit"],
            "GitUrl": git_url,
            "BranchName": event["multistage"]["branch"],
            "RepoName": event["multistage"]["repo"],
            "Version": event["version"],
            "FunctionRuntime": event["multistage"]["functionRuntime"]
        }
    }
    return lmd_args


def create_api_args(event):

    apigateway_resource = get_dict_ssm_parameter("apigateway_resource")
    runtime = event["runtime"]
    api_args = {
        "resources": event["multistage"]["entry"]["resources"],
        "LmdName": event["multistage"]["functionName"],
        "RestApiId": apigateway_resource[runtime]["RestApiId"],
        "AuthorizerId": apigateway_resource[runtime]["AuthorizerId"],
        "ApiResourceId": apigateway_resource[runtime]["ApiResourceId"],
        "ParentId": apigateway_resource[runtime]["ParentId"]
    }
    return api_args


def lambda_handler(event, context):
    print(event)
    # 1 处理lmd相关信息 返回lambdaArgs 参数用于运行codebuild
    lmd_args = create_lmd_args(event)
    # 2 处理apiGateway相关信息 返回apiGateWayArgs
    # RestApiId AuthorizerId ParentId 根据runtime进行获取
    api_args = create_api_args(event)
    iterator = {
        "index": 0,
        "currentStatus": "running"
    }
    lmdCounts = 1
    stackName = event["multistage"]["functionName"] + "-apiresource"
    return {
        "lmdCounts": lmdCounts,
        "iterator": iterator,
        "lambdaArgs": lmd_args,
        "apiGateWayArgs": api_args,
        "stackName": stackName
    }
