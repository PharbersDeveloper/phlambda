import os
import boto3
import random


def upload_code(zip_name):
    s3_client = boto3.client('s3')
    s3_client.upload_file(
        Bucket="ph-platform",
        Key="2020-11-11/cicd/ph-get-step-status/source/code.zip",
        Filename="/tmp/" + zip_name
    )


def zip_code():
    local_path_prefix = '/tmp'
    local_path = os.path.join(local_path_prefix, 'phlambda')
    for project in os.listdir(local_path):
        code_path = local_path + "/" + project + "/"

        # 复制ph_get_execution_status下的代码到当前目录下
        key_str = ""
        for key in os.listdir(code_path):
            cp_cmd = "cp -r " + code_path + key + " " + local_path_prefix
            # key =  "/tmp/" + ke
            os.popen(cp_cmd)
            key_str = key_str + key + " "

        os.chdir("/tmp")
        # 打包代码为code.zip
        random_code = random.randint(10000, 99999)
        zip_name = "code" + str(random_code) + ".zip"
        zip_cmd = "zip -r " + zip_name + " " + key_str
        os.system(zip_cmd)

        # 上传code到s3
        upload_code(zip_name)


if __name__ == '__main__':
    upload_code()