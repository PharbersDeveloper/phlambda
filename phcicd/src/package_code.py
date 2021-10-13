import os
import boto3
import random

def upload_code(zip_name, project_name):
    s3_client = boto3.client('s3')
    s3_client.upload_file(
        Bucket="ph-platform",
        Key="2020-11-11/cicd/"+ project_name +"/source/code.zip",
        Filename="/tmp/"  + zip_name
    )


def start_codebuild():
    client = boto3.client('codebuild')

    response = client.list_projects(
        sortOrder='ASCENDING'
    )
    codebuild_project = [
        "lmd-python3-codebuild",
        "lmd-nodejs-codebuild"
    ]
    for project in codebuild_project:
        client.start_build(
            projectName=project
        )


def  update_version(git_commit_version):
    # 修改README文件 填写版本号
    create_readme_file_cmd = "sed -i s/{git_commit_version}/" + git_commit_version + "/ /tmp/README.md"
    os.system(create_readme_file_cmd)


def download_resource(resource_path, download_path):
    s3_client = boto3.client('s3')
    s3_client.download_file(
        Bucket="ph-platform",
        Key=resource_path,
        Filename=download_path
    )


def zip_code(local_path, git_event):
    git_commit_version = git_event["git_commit_version"]
    codebuild_projects_name = ["python3",
                   "nodejs",
                   ]
    # 下载README.md
    README_s3_path = "2020-11-11/cicd/template/codebuild/README.md"
    README_file_path = "/tmp/README.md"
    download_resource(README_s3_path, README_file_path)
    # 替换git版本
    update_version(git_commit_version)

    for project in codebuild_projects_name:
        # 1下载对应buildspec.yaml
        buildsepc_s3_path = "2020-11-11/cicd/template/codebuild/" + project + "buildspec.yaml"
        buildsepc_file_path = "/tmp/" + project + "buildspec.yaml"
        download_resource(buildsepc_s3_path, buildsepc_file_path)
        # 2打包代码
        zip_cmd = "zip -r " + project + "code.zip /tmp/phlambda /tmp/README.md /tmp/" + project + "buildspec.yaml"
        os.system(zip_cmd)
        # 3代码上传到s3
        zip_name = project + "code.zip"
        project_name = "lmd" + project
        upload_code(zip_name, project_name)

