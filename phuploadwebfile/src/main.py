import boto3
import os
import zipfile
import urllib.parse


def lambda_handler(event, context):

    def upload_file_to_s3(bucket, s3_path, file):
        s3_client = boto3.client('s3')
        if s3_path == "pharbers.min.js":
            s3_path = "phbc.min.js"
        s3_client.upload_file(
            Bucket=bucket,
            Key=s3_path,
            Filename=file
        )

    def upload_dir_to_s3(bucket, s3_path, dir):

        for key in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, key)):
                upload_file_to_s3(bucket, os.path.join(s3_path, key), os.path.join(dir, key))
            else:
                upload_dir_to_s3(bucket, os.path.join(s3_path, key), os.path.join(dir, key))

    def upload_ember_to_s3(map):
        # 遍历对应信息
        for key in map.keys():
            bucket = map.get(key)
            s3_path = "/" + key
            file_path = "/tmp/micro-frontend/" + key + "/dist/"
            for key in os.listdir(file_path):
                if os.path.isfile(os.path.join(file_path, key)):
                    upload_file_to_s3(bucket, os.path.join(s3_path, key), os.path.join(file_path, key))
                else:
                    upload_dir_to_s3(bucket, os.path.join(s3_path, key), os.path.join(file_path, key))

    def upload_vue_to_s3(projects):
        for project in projects:
            file_path = "/tmp/micro-frontend/vue-web-components/" + project + "/dist/"
            file_suffix = "min.js"
            bucket = "ph-max-auto"
            for key in os.listdir(file_path):
                if key.endswith(file_suffix):
                    # print(os.path.join(file_path + key))
                    upload_file_to_s3(bucket, key, os.path.join(file_path + key))

    def upload_ember_project():
        # 上传项目有 bpcatelogpage，max, pharbers-web
        web_map = {
            "bpcatelogpage": "ph-max-auto",
            "max": "ph-max-auto",
            "pharbers-web": "ph-max-auto"
        }
        upload_ember_to_s3(web_map)


    def upload_vue_project():
        # vue项目 vue-basic-component vue-catelog-component vue-dag-component vue-echarts-component vue-excel-component
        # 只上传min.js文件 其中pharbers.min.js 文件 改成phbc.min.js上传
        vue_projects = ["vue-basic-component", "vue-catelog-component", "vue-dag-component", "vue-echarts-component", "vue-excel-component"]
        upload_vue_to_s3(vue_projects)

    def download_source(s3_path):
        s3_client = boto3.client('s3')
        filename = s3_path.split("/")[-1]
        local_path = "/home/hbzhao/cicd/web/" + filename
        s3_client.download_file(
            Bucket="ph-platform",
            Key=s3_path,
            Filename=local_path
        )
        # 解压代码zip文件
        unzip_file(local_path)
        return filename

    def unzip_file(path):
        with zipfile.ZipFile(path) as zf:
            zf.extractall(path=os.path.dirname(path))

    print(event)
    # 首先解析上传zip文件的位置 下载代码 进行解压
    key = urllib.parse.unquote(event['Records'][0]['s3']['object']['key'])
    download_source(key)
    # 上传ember项目的文件
    upload_ember_project()
    # 上传vue项目的文件
    upload_vue_project()
