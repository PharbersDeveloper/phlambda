import json
import boto3
from clickhouse_driver import Client
from boto3.dynamodb.conditions import Key


'''
删除创建的中间文件，文件都从 dynamodb 找，并按照规则拼出路径
args = {
    "traceId": "alfred-resource-creation-traceId",
    "projectId": "ggjpDje0HUC2JW",
    "projectName": "demo",
    "owner": "alfred",
    "showName": "alfred"
}
'''

# job key: f"2020-11-11/jobs/python/phcli/{projectName}{flowVersion}"
# dataset key:  f"2020-11-11/lake/pharbers/{projectId}/{ds_name}/"
# sm.json key:  f"2020-11-11/jobs/statemachine/pharbers/{projectName}{flowVersion}"
# clickhouse_tablename = f"{projectId}_{ds_name}"


class ResourceDeletion:

    def __init__(self, host):
        self.dynamodb = boto3.client("dynamodb")
        self.s3 = boto3.resource("s3")
        self.clickhouse = Client(host=host, port=9000)

    def del_clickhouse(self, table_name):
        sql = f"DROP TABLE IF EXISTS `default`.`{table_name}`"
        self.clickhouse.execute(sql)
        # pass

    def del_s3_obj(self, key):
        bucket = self.s3.Bucket("ph-platform")
        bucket.objects.filter(Prefix=key).delete()

    def ls_s3_key(self, file_key):
        s3 = boto3.client("s3")
        response = s3.list_objects_v2(
            Bucket="ph-platform",
            Prefix=file_key,
            MaxKeys=100)
        return [i.get('Key').replace(file_key, '').split("/")[0]
                for i in response.get('Contents', {})]

    def run(self, projectId, projectName, **kwargs):
        dataset_key = f"2020-11-11/lake/pharbers/{projectId}"
        job_key = f"2020-11-11/jobs/python/phcli/{projectName}_{projectName}"
        sm_json_key = f"2020-11-11/jobs/statemachine/pharbers/{projectName}_{projectName}"
        for table_name in self.ls_s3_key(dataset_key):
            print(table_name)
            if table_name:
                self.del_clickhouse(f"{projectId}_{table_name}")

        for key in [dataset_key, job_key, sm_json_key]:
            self.del_s3_obj(key)


def lambda_handler(event, context):
    print(event)
    clickhouse_ip = event.get("resources").get("olap").get("PrivateIp")
    ResourceDeletion(clickhouse_ip).run(**event)
    return True

