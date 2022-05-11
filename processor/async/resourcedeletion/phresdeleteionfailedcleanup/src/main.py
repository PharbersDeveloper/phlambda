import time
import boto3

'''
这个函数实现两件事情：
1. 将错误的信息写入 notification 中
2. 将错误的被删除的 index 重新写回 dynamodb 中
    所有的信息都在 result 中存放

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "projectName.$": "$.common.projectName",
        "resources": {

        },
        "result": {
            "datasets": [
                {
                    "name": "test_name",
                    "cat": "intermediate",
                    "format": "parquet"
                }
            ],
            "script": {
                "id": "String",
                "jobName": "String",
                "actionName": "String",
                "flowVersion": "developer",
                "inputs": "[]",
                "output": "{}"
            },
            "links": [{
                "id": "",
                ...
            }]，
            "errors": {
                "Error": "Exception",
                "Cause": ""
                }
        }
    }
'''


class CleanUp:
    name_list = []
    del_list = []
    dynamodb = boto3.resource("dynamodb", region_name="cn-northwest-1")

    def put_item(self, table_name, item):
        table = self.dynamodb.Table(table_name)
        response = table.put_item(
            Item=item
        )

    def run(self, datasets, scripts, links, **kwargs):
        for dataset in datasets:
            self.put_item("dataset", dataset)
        for script in scripts:
            self.put_item("dagconf", script)
        for link in links:
            self.put_item("dag", link)


def lambda_handler(event, context):
    # 1. 将错误的信息写入 notification 中
    # 2. 将错误的被删除的 index 重新写回 dynamodb 中
    #     所有的信息都在 result 中存放
    result = event.get("result")
    CleanUp().run(**result)
    return True

