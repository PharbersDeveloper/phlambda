import os
import json
import copy
import boto3
from itertools import product

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
                destinations: [
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


def download_s3_dir(bucket_name, dir_key, dist_local_path):
    bucket = s3_resource.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=dir_key):
        if not os.path.exists(dist_local_path):
            os.makedirs(dist_local_path)
        if not obj.key.endswith("/"):
            if not os.path.exists("/".join((dist_local_path + obj.key.replace(dir_key + "/", "")).split("/")[:-1])):
                os.makedirs("/".join((dist_local_path + obj.key.replace(dir_key + "/", "")).split("/")[:-1]))
            download_s3_file(bucket_name, obj.key, dist_local_path + obj.key.replace(dir_key + "/", ""))


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


def read_local_json_file(local_path):
    with open(local_path, 'r', encoding='utf8')as f:
        json_data = json.load(f)
    return json_data


def create_devops_file_map(files, dist_local_path, destinations, modifications):
    def deal_resolve(file_name, file_modify_maps):
        if file_modify_maps:
            for file_modify_map in file_modify_maps:
                if file_modify_map["source"] == file_name:
                    file_name = file_modify_map["target"]
        return file_name

    # 获取 dist_local_path 下的所有文件
    file_names = []
    for root, dirs, file in os.walk(dist_local_path):
        for name in file:
            file_names.append(os.path.join(root, name).replace(dist_local_path, ""))
    deal_file_names = []
    # 判断files下的文件后缀 如果为空则上传文件夹下所有文件
    if files:
        for file in files:
            deal_file_name = list(i for i in file_names if ".".join(i.split(".")[1:]) == file.strip("*."))
            deal_file_names.extend(deal_file_name)
    else:
        deal_file_names = copy.deepcopy(file_names)
    # 获取destination 下的target_s3_dir
    local_s3_maps = []
    result = product(deal_file_names, destinations.copy())
    for i in list(result):
        s3_file_name = deal_resolve(i[0], modifications)
        local_s3_maps.append({
            "bucket": i[1]["bucket"],
            "key": i[1]["key"] + s3_file_name,
            "local_path": dist_local_path + i[0]
        })
    print(local_s3_maps)
    # 返回需要上传的本地文件路径和线上
    return local_s3_maps


def lambda_handler(event, context):
    print(event)
    runtime = event["runtime"]
    deploy_s3_paths = []
    componentArgs = event["componentArgs"]
    for componentArg in componentArgs:
        dist_s3_source = "/".join(componentArg["s3ComponentPath"].split("/")[3:])
        dist_local_path = "/tmp/" + componentArg["componentPrefix"] + "/dist/"
        # 下载s3ComponentPath 目录下的dist
        download_s3_dir("ph-platform", dist_s3_source, dist_local_path)
        # 读取.devops文件 通过devops/runtime/prefix
        frontend_devops_data = read_local_json_file(dist_local_path + ".devops")
        # files 如果files为空则获取所有prefix下文件'
        # 获取本地文件和上传位置的map
        # destination 为s3目标目录
        local_s3_maps = create_devops_file_map(
            frontend_devops_data["devops"][runtime]["files"],
            dist_local_path,
            frontend_devops_data["devops"][runtime]["destinations"],
            frontend_devops_data["devops"][runtime].get("modifications")
        )
        print(local_s3_maps)
        # 上传deploy文件
        for local_s3_map in local_s3_maps:
            upload_s3_file(local_s3_map["bucket"], local_s3_map["key"], local_s3_map["local_path"])
        deploy_s3_paths.extend(local_s3_maps)

    return deploy_s3_paths
