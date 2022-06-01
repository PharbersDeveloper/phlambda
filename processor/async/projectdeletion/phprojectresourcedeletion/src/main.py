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
    dynamodb = boto3.resource("dynamodb")
    s3 = boto3.resource("s3")
    clickhouse = Client()

    def del_clickhouse(self, table_name):
        sql = f"DROP TABLE IF EXISTS `{table_name}`"
        self.clickhouse.execute(sql)

    def query_item(self, table, index):
        table = self.dynamodb.Table(table)
        response = table.query(
            IndexName=index,
            KeyConditionExpression=Key('projectId').eq(self.projectId)
        )
        return response.get("Items")

    def del_item(self, table_name, col_name, col_value):
        table = self.dynamodb.Table(table_name)
        table.delete_item(
            Key={
                col_name: col_value,
                "projectId": self.projectId
            }
        )

    def del_s3_obj(self, key):
        bucket = self.s3.Bucket("ph-platform")
        bucket.objects.filter(Prefix=key).delete()

    def ls_s3_key(self, file_key):
        response = self.s3.list_objects_v2(
            Bucket="ph-platform",
            Prefix=file_key,
            MaxKeys=100)
        return [i.get('Key') for i in response.get('Contents', {})]

    def run(self, projectId, projectName, **kwargs):
        self.projectId = projectId
        dy_datasets = self.query_item("dataset", "dataset-projectId-traceId-index")
        dy_dags = self.query_item("dag", "dag-projectId-traceId-index")
        dy_dagconfs = self.query_item("dagconf", "dagconf-projectId-traceId-index")

        for ds in dy_datasets:
            id = ds.get("id")
            self.del_item(table_name="dataset", col_name="id", col_value=id)

        for dag in dy_dags:
            sortVersion = dag.get("sortVersion")
            self.del_item(table_name="dag", col_name="sortVersion", col_value=sortVersion)

        for dagconf in dy_dagconfs:
            jobName = dagconf.get("jobName")
            dagconf_jobPath = dagconf.get("jobPath")
            jobtype = dagconf_jobPath.split('/')[-1]
            jobPath = dagconf_jobPath.replace(jobtype, "")
            self.del_item(table_name="dagconf", col_name="jobName", col_value=jobName)
            #
            # file_name_list = self.ls_s3_key(jobPath)
            # name_list = [file_name.split('/')[-1] for file_name in file_name_list]
            # if traceId in name_list:
            #     for key in file_name_list:
            #         self.del_s3_obj(key)

        dataset_key = f"2020-11-11/lake/pharbers/{projectId}/"
        job_key = f"2020-11-11/jobs/python/phcli/{projectName}/"
        sm_json_key = f"2020-11-11/jobs/statemachine/pharbers/{projectName}/"
        for key in [dataset_key, job_key, sm_json_key]:
            self.del_s3_obj(key)


def lambda_handler(event, context):
    ResourceDeletion().run(**event)
    return True
