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
    name_list = []
    del_list = []
    s3 = boto3.client('s3')
    dynamodb = boto3.resource("dynamodb", region_name="cn-northwest-1",
                               aws_access_key_id="AKIAWPBDTVEANKEW2XNC",
                               aws_secret_access_key="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")

    def query_dataset(self, name):
        table = self.dynamodb.Table("dataset")
        response = table.query(
            IndexName='dataset-projectId-name-index',
            KeyConditionExpression=Key('projectId').eq(self.projectId) & Key("name").eq(name),
        )
        return response.get("Items")

    def query_dag(self):
        table = self.dynamodb.Table("dag")
        response = table.query(
            KeyConditionExpression=Key('projectId').eq(self.projectId),
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
    # print(del_item('fe1e73a8b0fd44ba93aa0cf6b5ee2f2112345', "fe1e73a8bTEstdel"))

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

    def check_dag_item(self):
        dag_item = self.query_dag()
        for dag in dag_item:
            ctype = dag.get("ctype")
            representId = dag.get("representId")
            sortVersion = dag.get("sortVersion")
            if ctype == "node" and representId in self.del_list:
                self.del_item(table_name="dag", col_name="sortVersion", col_value=sortVersion)

            if ctype == "link":
                cmessage = json.loads(dag.get("cmessage"))
                sourceId = cmessage.get("sourceId")
                targetId = cmessage.get("targetId")
                if sourceId in self.del_list or targetId in self.del_list:
                    self.del_item(table_name="dag", col_name="sortVersion", col_value=sortVersion)

    def run(self, projectId, datasets, scripts, traceId, **kwargs):

        self.projectId = projectId
        self.name_list.append(scripts.get("actionName"))
        for dataset in datasets:
            self.name_list.append(dataset.get("name"))

        for name in self.name_list:
            dy_dataset = self.query_dataset(name)
            if dy_dataset:
                self.del_list.append(dy_dataset[0].get("id"))

        for id in self.del_list:
            self.del_item(table_name="dataset", col_name="id", col_value=id)

        self.check_dag_item()
        jobName = scripts.get("jobName")
        actionName = scripts.get("actionName")
        key = "2020-11-11/jobs/python/phcli/" + jobName + actionName
        file_name_list = self.ls_s3_key(key)
        for file_name in file_name_list:
            if file_name == traceId:
                self.del_s3_obj(key)


def lambda_handler(event, context):
    CleanUp().run(**event)
    # 1. 如果dataset name在dataset中存在，删除
    # 2. 如果scripts name在dataset中存在，删除
    # 3. 如果dag表中，ctype = node && represent-id 为上诉中的已经被删除的节点删除
    # 4. 如果dag表中，ctype = node && cmessage 中 sourceId 或者 targetId 为上述中的删除节点的删除
    # 5. 删除s3中目标文件夹的文件
    #   5.1 每一个生成过程都给一个TraceID命名的文件，如果文件名一样，删除，如果文件不一样说明时别人创建的不能删除
    return True
