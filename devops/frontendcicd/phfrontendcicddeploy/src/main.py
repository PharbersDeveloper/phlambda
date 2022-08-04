import boto3
from boto3.dynamodb.conditions import Key

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')
'''
这个函数只做一件事情，检查参数是否合法
args:
    event = {
        "version": "0-0-1",
        "publisher": "赵浩博",
        "runtime": "dev/v2/prod",
        "frontend": {
            "stackName": component["name"] + "codebuild",
            "componentPrefix": component["prefix"],
            "buildSpec": buildSpec,
            "codebuildCfn": codebuild_cfn_path,
            "componentName": component["prefix"].split("/")[-1],
            "branchName": frontend["branch"],
            "repoName": frontend["repo"],
            "version": event["version"],
            "runtime": event["runtime"],
            "gitCommit": event["commit"],
            "gitUrl": git_url,
            "s3ComponentPath": "s3://ph-platform/2020-11-11/cicd/" + component["prefix"] + event["version"]}
        }
    {
    "devops": {
        prod: {
            prefix: dist(default)
            files: ["*.js"],
            destination: [
                   {
                        bucket: "ph-platform"
                        key: "2020-11-11/cicd/test/offweb-model-helper/"
                   }
               ],
            resolve: ""
            }
        },
        "prod": {
        
        },
        "dev": {
        
        }
    }
'''


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


def check_parameter(event):
    print(1)
    return True


def lambda_handler(event, context):
    print(event)
    # 下载s3ComponentPath 目录下的dist
    # 获取.devops文件 通过devops/runtime/prefix
    # files 如果files为空则获取所有prefix下文件
    # destination 为s3目标目录
    return check_parameter(event)

