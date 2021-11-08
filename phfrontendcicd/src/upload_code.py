import os
import boto3
import random


def upload_code(zip_name, project_name):
    s3_client = boto3.client('s3')
    s3_client.upload_file(
        Bucket="ph-platform",
        Key="2020-11-11/cicd/" + project_name + "/source/code.zip",
        Filename="/tmp/"  + zip_name
    )


def start_codebuild():
    client = boto3.client('codebuild')
    client.start_build(
        projectName="offweb-codebuild"
    )


def download_resource(resource_path, download_path):
    s3_client = boto3.client('s3')
    s3_client.download_file(
        Bucket="ph-platform",
        Key=resource_path,
        Filename=download_path
    )

def  update_version(git_commit_version):
    # 修改README文件 填写版本号
    create_readme_file_cmd = "sed -i s/{git_commit_version}/" + git_commit_version + "/ /tmp/README.md"
    os.system(create_readme_file_cmd)


def zip_code(local_path, git_event):

    git_commit_version = git_event["git_commit_version"]

    repo = git_event.get("merge_repository_to")
    # 删除.git文件
    rm_cmd = "rm -rf /tmp/"+ repo +"/.git"
    os.system(rm_cmd)
    # 下载README.md
    # README_S3_PATH = "2020-11-11/cicd/template/codebuild/README.md"
    # README_FILE_PATH = "/tmp/README.md"
    README_S3_PATH = os.getenv("README_S3_PATH")
    README_FILE_PATH = os.getenv("README_FILE_PATH")
    download_resource(README_S3_PATH, README_FILE_PATH)
    print("下载README.md成功")
    # 替换git版本
    update_version(git_commit_version)
    print("替换git版本成功")

    # 1下载对应buildspec.yaml
    # BUILDSEPC_S3_PATH = "2020-11-11/cicd/template/codebuild/frontendbuildspec.yaml"
    # BUILDSEPC_FILE_PATH = "/tmp/frontendbuildspec.yaml"
    BUILDSEPC_S3_PATH = os.getenv("BUILDSEPC_S3_PATH")
    BUILDSEPC_FILE_PATH = os.getenv("BUILDSEPC_FILE_PATH")
    download_resource(BUILDSEPC_S3_PATH, BUILDSEPC_FILE_PATH)
    print("下载对应buildspec.yaml成功")

    # 2打包代码
    os.chdir("/tmp")
    zip_cmd = "zip -r frontendcode.zip micro-frontend README.md frontendbuildspec.yaml"
    os.system(zip_cmd)
    print("2打包代码成功")

    # 3代码上传到s3
    zip_name = "frontendcode.zip"
    project_name = "offweb"
    upload_code(zip_name, project_name)
    print("代码上传到s3成功")



if __name__ == '__main__':
    git_event = {'event_key': 'pr:merged', 'event_type': 'MERGED', 'time': '2021-11-02T15:34:46+0800', 'operator_name': 'hbzhao', 'merge_repository_from': 'micro-frontend', 'merge_branch_from': 'developer', 'merge_repository_to': 'micro-frontend', 'merge_branch_to': 'master', 'merge_request_user': 'hbzhao', 'git_commit_version': '1807c1802d7', 'merge_reviewers': []}
    local_path = "/home/hbzhao/PycharmProjects/pythonProject/micro-frontend"
    zip_code(local_path, git_event)
