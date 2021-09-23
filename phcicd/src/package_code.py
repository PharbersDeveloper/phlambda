import os
import boto3
import random

def upload_code(zip_name, project_name):
    s3_client = boto3.client('s3')
    s3_client.upload_file(
        Bucket="ph-platform",
        Key="2020-11-11/cicd/"+ project_name +"/source/code.zip",
        Filename="/tmp/" + zip_name
    )

def start_codebuild():
    client = boto3.client('codebuild')

    response = client.list_projects(
        sortOrder='ASCENDING'
    )

    for project in response['projects']:
        if project == "codebuild-manager-phnoticeemail-V77NNXP745NE":
            client.start_build(
                projectName=project,
            )

def zip_code(local_path):
    for project_name in os.listdir(local_path):
        if project_name == "phnoticeemail":
            code_path = local_path + "/" + project_name + "/"
            if os.path.isdir(code_path):
                # 创建文件夹
                mkdir_cmd = "mkdir /tmp/" + project_name
                os.system(mkdir_cmd)

                # 复制ph_get_execution_status下的代码到当前目录下
                key_str = ""
                for key in os.listdir(code_path):
                    if os.path.isdir(code_path + key):
                        cp_cmd = "cp -r " + code_path + key + "/" + " /tmp/" + project_name + "/"
                    else:
                        cp_cmd = "cp -r " + code_path + key + " /tmp/" + project_name + "/"
                    os.popen(cp_cmd)
                    key_str = key_str + key + " "

                os.chdir("/tmp/" + project_name)
                # 打包代码为code.zip
                random_code = random.randint(10000,99999)
                zip_name = "code" + str(random_code) + ".zip"
                zip_cmd = "zip -r "+ zip_name +" " + key_str
                os.system(zip_cmd)

                # 上传code到s3
                upload_code(zip_name, project_name)

if __name__ == '__main__':
    local_path = "/home/hbzhao/PycharmProjects/pythonProject/phlambda"
    zip_code(local_path)