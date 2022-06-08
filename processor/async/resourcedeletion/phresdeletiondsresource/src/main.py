import json
import boto3
from boto3.dynamodb.conditions import Attr
import os
from ClieckHouse import ClickHouse

'''
删除ds相关的数据信息
1. 一定是 先删除 clickhouse 中的 sample
2. 再删除 S3 中的数据

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "resources": {
    
        },
        "datasets.$": [{
            "id": "",
                ....
        }]
    }
'''


def del_s3_job_dir(bucket_name, s3_dir):

    s3_client = boto3.resource('s3')
    objects_to_delete = s3_client.list_objects(Bucket=bucket_name, Prefix=s3_dir)

    delete_keys = {'Objects' : []}
    delete_keys['Objects'] = [{'Key': k} for k in [obj['Key'] for obj in objects_to_delete.get('Contents', [])]]
    print(delete_keys)
    s3_client.delete_objects(Bucket="ph-platform", Delete=delete_keys)


def __create_clickhouse(resource):
    olap = resource.get("olap")
    ip = olap.get("PrivateIp")
    return ClickHouse(host=ip, port=os.environ["CLICKHOUSE_PORT"])


def lambda_handler(event, context):
    print(event)
    clickhouse = __create_clickhouse(event["resources"])
    # 从script 中获取 jobPath 进行删除
    for dataset in event["datasets"]:
        tableName = event["projectId"] + "_" + dataset["name"]
        clickhouse.exec_ddl_sql(f"""DROP TABLE IF EXISTS {os.environ["CLICKHOUSE_DB"]}.`{tableName}`""")

    for dataset in event["datasets"]:
        path = "2020-11-11/lake/pharbers/" + event["projectId"] + "/" + dataset["name"] + "/"
        print(path)
        del_s3_job_dir("ph-platform", path)

    return True
