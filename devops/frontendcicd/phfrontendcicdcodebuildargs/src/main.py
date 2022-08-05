import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
'''
这个函数只做一件事情，检查参数是否合法
args:
    event = {
        "version": "0-0-1",
        "publisher": "赵浩博",
        "runtime": "prod"
        "frontend": {
            "branch": "PBDP-3235-cicd",
            "commit": "184d0599303ccaa537417610c0dd6b929fe3a8a5",
            "repo": "micro-frontend",
            "components": [
                {
                    "prefix": "client-helper/offweb-model-helper",
                }
            ]
            "required": true
        }
    }
'''
codebuild_cfn_path = "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cicd/template/phfront-codebuild.yaml"
git_url = "http://cicd:Abcde196125@192.168.53.179:7990/scm/lgc/phlambda.git"
buildSpec = {
    "client-helper": "helperFrontBuildspec",
    "iframe-web-components": "iframeFrontBuildspec",
    "vue-web-components": "vueFrontBuildspec",
    "web-shell": "emberFrontBuildspec"
}

def create_component_args(event):
    component_args = []
    frontend = event["frontend"]
    for component in frontend["components"]:
        component_arg = {
            "stackName": component["prefix"].split("/")[-1] + "codebuild",
            "componentPrefix": component["prefix"],
            "buildSpec": buildSpec[component["prefix"].split("/")[0]],
            "codebuildCfn": codebuild_cfn_path,
            "componentName": component["prefix"].split("/")[-1],
            "branchName": frontend["branch"],
            "repoName": frontend["repo"],
            "version": event["version"],
            "runtime": event["runtime"],
            "gitCommit": event["commit"],
            "gitUrl": git_url,
            "s3ComponentPath": "s3://ph-platform/2020-11-11/cicd/frontendcicd/" + component["prefix"] + event["version"]
        }
        component_args.append(component_arg)

    return component_args


def lambda_handler(event, context):
    print(event)
    # 计算要发布的component数量
    componentCounts = len(event["frontend"]["components"])
    # 设置iterator
    iterator = {
        "index": 0,
        "currentStatus": "running"
    }
    # 处理lambda相关信息
    componentArgs = create_component_args(event)
    return {
        "componentCounts": componentCounts,
        "iterator": iterator,
        "componentArgs": componentArgs,
    }

