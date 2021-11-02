import json
import boto3
import os
import urllib.parse
import re
import psycopg2

def lambda_handler(event, context):

    def upload_file_to_s3(bucket, s3_path, file):
        s3_client = boto3.client('s3')
        print(s3_path)
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
            s3_path = "/"
            file_path = "/tmp/micro-frontend/" + key
            for key in os.listdir(file_path):
                if os.path.isfile(os.path.join(file_path, key)):
                    upload_file_to_s3(bucket, os.path.join(s3_path, key), os.path.join(file_path, key))
                else:
                    upload_dir_to_s3(bucket, os.path.join(s3_path, key), os.path.join(file_path, key))

    def upload_vue_to_s3(projects):
        for project in projects:
            file_path = "/tmp/micro-frontend/" + project
            file_suffix = "min.js"
            s3_path = "/"
            bucket = "components.pharbers.com"
            for key in os.listdir(file_path):
                if key.endswith(file_suffix):
                    if key == "pharbers.min.js":
                        key == "phbc.min.js"
                    upload_file_to_s3(bucket, s3_path, os.path.join(file_path + key))
        pass

    def upload_vue_project():
        # 上传项目有 bpcatelogpage，max, pharbers-web
        web_map = {
            "bpcatelogpage": "general.pharbers.com",
            "max": "deploy.pharbers.com",
            "pharbers-web": "www.pharbers.com"
        }
        upload_ember_to_s3(web_map)
        pass

    def upload_ember_file():
        # vue项目 vue-basic-component vue-catelog-component vue-dag-component vue-echarts-component vue-excel-component
        # 只上传min.js文件 其中pharbers.min.js 文件 改成phbc.min.js上传
        vue_projects = ["vue-basic-component", "vue-catelog-component", "vue-dag-component", "vue-echarts-component", "vue-excel-component"]
        upload_vue_to_s3(vue_projects)
        pass

    def download_source():
        pass

    # 首先下载代码
    # 上传ember项目的文件
    # 上传vue项目的文件