import json
import boto3
from boto3.dynamodb.conditions import Attr, Key

'''
这个函数只做一件事情，检查参数是否合法
args:
    event = {
        "common": {
            "traceId": "alfred-resource-creation-traceId",
            "projectId": "ggjpDje0HUC2JW",
            "projectName": "demo",
            "owner": "alfred",
            "showName": "alfred"
        },
        "action": {
            "cat": "createDataset",
            "desc": "create intermediate dataset",
            "comments": "something need to say",
            "message": "something need to say",
            "required": true
        },
        "datasets": [
            {
                "name": "test_name"
            }
        ],
        "script": {
            "actionName": "compute_C2",
        },
        "notification": {
            "required": true
        }
    }
'''


dynamodb = boto3.resource("dynamodb", region_name="cn-northwest-1")


# def scan_table(project_id, ds_name, table_name, item_name):
#     try:
#         table = dynamodb.Table(table_name)
#         result = table.scan(
#             FilterExpression=Attr(item_name).eq(ds_name) & Attr("projectId").eq(project_id),
#             Limit=10,
#         )
#         return result.get("Items")
#     except:
#         return None


def query_item(table, projectId, index=None, col_name=None, col_value=None):
    table = dynamodb.Table(table)
    if index:
        response = table.query(
            IndexName=index,
            KeyConditionExpression=Key('projectId').eq(projectId) & Key(col_name).eq(col_value),
        )
    else:
        response = table.query(
            KeyConditionExpression=Key('projectId').eq(projectId)
        )
    return response.get("Items")


class Check:

    ds_sc = False

    def check_datasets_scripts(self, data):
        projectId = data.get("common").get("projectId")
        datasets = data.get("datasets", [])
        scripts = data.get("scripts", [])
        if not isinstance(datasets, list):
            raise Exception('datasets type error')
        for dataset in datasets:
            ds_name = dataset.get("name", '')
            if not ds_name:
                raise Exception('datasets missing name field')
            if query_item("dataset", projectId, "dataset-projectId-name-index", "name", ds_name):
                raise Exception('datasets name already exits')
            self.ds_sc = True
        for script in scripts:
            script_name = script.get("actionName")
            if not script_name:
                raise Exception('scripts missing name field')
            if [i for i in query_item("dagconf", projectId) if i.get("actionName") == script_name]:
                raise Exception('dagconf actionName already exits')
            self.ds_sc = True

    def check_parameter(self, data):

        # 1. common 必须存在
        if not data.get("common"):
            raise Exception('common not exits')

        # 2. action 必须存在
        if not data.get("action"):
            raise Exception('action not exits')

        # 3. notification 必须存在
        if not data.get("notification"):
            raise Exception('notificaiton not exits')

        # 4. datasets 和 scripts 必须存在一个
        self.check_datasets_scripts(data)

        if not self.ds_sc:
            raise Exception('datasets scripts not exits')
        return True


def lambda_handler(event, context):
    return Check().check_parameter(event)

    # 1. common 必须存在
    # 2. action 必须存在
    # 3. notification 必须存在
    # 4. datasets 和 scripts 必须存在一个
    #   4.1 如果dataset存在，name 都必须存在，并判断类型
    #   4.2 如果scripts存在，actionName 都必须存在，并判断类型
    # 5. 输入的datasets name 必须存在
    # 6. 输入的script 的 actionName 必须存在
    # return true
