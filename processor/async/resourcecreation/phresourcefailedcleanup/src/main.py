import json
import boto3
from boto3.dynamodb.conditions import Key

'''
这个函数清理已经操作的东西，保证操作的原子性
args = {
    "traceId": "String",
    "projectId": "String",
    "owner": "String",
    "showName": "String",
    "traceId": "String",
    "projectId": "String",
    "owner": "String",
    "showName": "String",
    "datasets": [
        {
            "id": "String",
            "name": "String",
            "cat": "intermediate",
            "format": "parquet"
        }
    ],
    "scripts": {
        "id": "String",
        "jobName": "String",
        "actionName": "String",
        "flowVersion": "developer",
        "inputs": "[]",
        "output": "{}"
    },
    "errors": {
        "Error": "Exception",
        "Cause": ""
    }
}
'''


class CleanUp:
    s3 = boto3.client('s3')
    dynamodb = boto3.resource("dynamodb", region_name="cn-northwest-1",
                               aws_access_key_id="AKIAWPBDTVEANKEW2XNC",
                               aws_secret_access_key="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")

    # def query_dag(self):
    #     table = self.dynamodb.Table("dag")
    #     response = table.query(
    #         KeyConditionExpression=Key('projectId').eq(self.projectId),
    #     )
    #     return response.get("Items")

    # def check_dag_item(self):
    #     dag_item = self.query_dag()
    #     for dag in dag_item:
    #         ctype = dag.get("ctype")
    #         representId = dag.get("representId")
    #         sortVersion = dag.get("sortVersion")
    #         if ctype == "node" and representId in self.del_list:
    #             self.del_item(table_name="dag", col_name="sortVersion", col_value=sortVersion)
    #
    #         if ctype == "link":
    #             cmessage = json.loads(dag.get("cmessage"))
    #             sourceId = cmessage.get("sourceId")
    #             targetId = cmessage.get("targetId")
    #             if sourceId in self.del_list or targetId in self.del_list:
    #                 self.del_item(table_name="dag", col_name="sortVersion", col_value=sortVersion)

    def query_item(self, table, index, traceId):
        table = self.dynamodb.Table(table)
        response = table.query(
            IndexName=index,
            KeyConditionExpression=Key('projectId').eq(self.projectId) & Key("traceId").eq(traceId),
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
        response = self.s3.delete_object(
            Bucket="ph-platform",
            Key=key,
        )

    def ls_s3_key(self, file_key):
        response = self.s3.list_objects_v2(
            Bucket="ph-platform",
            Prefix=file_key,
            MaxKeys=100)
        return [i.get('Key') for i in response.get('Contents', {})]

    def run(self, projectId, traceId, **kwargs):

        self.projectId = projectId
        dy_dataset = self.query_item("dataset", "dataset-projectId-traceId-index", traceId)
        dy_dag = self.query_item("dag", "dag-projectId-traceId-index", traceId)
        dy_dagconf = self.query_item("dagconf", "dagconf-projectId-traceId-index", traceId)

        if dy_dataset:
            id = dy_dataset[0].get("id")
            self.del_item(table_name="dataset", col_name="id", col_value=id)

        if dy_dag:
            sortVersion = dy_dag[0].get("sortVersion")
            self.del_item(table_name="dag", col_name="sortVersion", col_value=sortVersion)

        if dy_dagconf:
            jobName = dy_dagconf[0].get("jobName")
            dagconf_jobPath = dy_dagconf[0].get("jobPath")
            jobtype = dagconf_jobPath.split('/')[-1]
            jobPath = dagconf_jobPath.replace(jobtype, "")
            print(jobPath)
            self.del_item(table_name="dagconf", col_name="jobName", col_value=jobName)

            file_name_list = self.ls_s3_key(jobPath)
            name_list = [file_name.split('/')[-1] for file_name in file_name_list]
            if traceId in name_list:
                for key in file_name_list:
                    self.del_s3_obj(key)


def lambda_handler(event, context):
    CleanUp().run(**event)
    # 1. 如果dataset name在dataset中存在，删除
    # 2. 如果scripts name在dataset中存在，删除
    # 3. 如果dag表中，ctype = node && represent-id 为上诉中的已经被删除的节点删除
    # 4. 如果dag表中，ctype = link && cmessage 中 sourceId 或者 targetId 为上述中的删除节点的删除
    # 5. 删除s3中目标文件夹的文件
    #   5.1 每一个生成过程都给一个TraceID命名的文件，如果文件名一样，删除，如果文件不一样说明时别人创建的不能删除
    return True
