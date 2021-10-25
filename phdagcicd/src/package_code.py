import os
import boto3
import random

def upload_file_to_s3(bucket, path, file):
    s3_client = boto3.client('s3')
    s3_client.upload_file(
        Bucket=bucket,
        Key=path,
        Filename=file
    )

def upload_dir_to_s3(bucket, path, dir):

    path = path if path.endswith("/") else path+"/"
    dir = dir if dir.endswith("/") else dir+"/"

    for key in os.listdir(dir):
        if os.path.isfile(dir+key):
            upload_file_to_s3(bucket, path+key, dir+key)
        else:
            upload_dir_to_s3(bucket, path+key, dir+key)


def upload_code(local_path, git_event):
    branch_name = git_event.get("branch_name")
    os.system("cd " + local_path)
    for key in os.listdir(local_path):
        if os.path.isfile(key):
            bucket = "s3fs-ph-airflow"
            path = "airflow/dags/" + key
            file = local_path + key
            upload_file_to_s3(bucket, path, file)
        if os.path.isdir(key):
            bucket = "ph-platform"
            path = "2020-11-11/jobs/python/phcli/" + branch_name + "/"
            dir = local_path + key
            upload_dir_to_s3(bucket, path, dir)

