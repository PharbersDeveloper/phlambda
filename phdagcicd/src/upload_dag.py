import os
import boto3
import random


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


def upload_code(local_path, git_event):

    branch_name = git_event.get("branch_name")
    print(branch_name)
    os.system("cd " + local_path)
    dag_local_path = os.path.join(local_path, "phdags", branch_name)
    for key in os.listdir(dag_local_path):
        if os.path.isfile(os.path.join(dag_local_path, key)):
            os.getenv("FLOW_BUCKET")
            bucket = os.getenv("FLOW_BUCKET")
            os.getenv("FLOW_FILE_PATH")
            s3_path = os.getenv("FLOW_FILE_PATH")
            file = os.path.join(dag_local_path, key)
            print(file)
            upload_file_to_s3(bucket, os.path.join(s3_path, key), file)
        if os.path.isdir(os.path.join(dag_local_path, key)):
            os.getenv("DAG_BUCKET")
            bucket = os.getenv("DAG_BUCKET")
            os.getenv("DAG_JOBS_PATH")
            s3_path = os.getenv("DAG_JOBS_PATH") + branch_name + "/"
            dir = os.path.join(dag_local_path, key)
            print(dir)
            upload_dir_to_s3(bucket, os.path.join(s3_path, key), dir)

if __name__ == '__main__':
    git_event = {'event_key': 'repo:refs_changed', 'event_type': 'UPDATE', 'time': '2021-10-25T16:18:52+0800', 'operator_name': 'hbzhao', 'repository_name': 'phmax', 'branch_name': 'cicd_flow_max_20211026'}
    local_path = "/home/hbzhao/PycharmProjects/pythonProject/phmax"
    upload_code(local_path, git_event)
