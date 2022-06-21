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
                "name": "test_name",
                "cat": "intermediate",
                "format": "parquet"
            }
        ],
        "scripts": {
                "name": "compute_C2",
                "flowVersion": "developer",
                "inputs": "[]",
                "output": "{}"
            },
        "notification": {
            "required": true
        },
        "result": {
            "datasets": [""],
            "scripts": [""],
            "links": [""]
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

    def checkdata(self, data, value):
        if not set(value) <= set(list(data.keys())):
            raise Exception('datasets or scripts Missing field')
        self.ds_sc = True

    def checktype(self, data):
        if data:
            inputs = json.loads(data.get('inputs'))
            if not isinstance(inputs, list):
                raise Exception('scripts type error')

    def check_datasets_scripts(self, data):
        ds_value = ['cat', 'format', 'name']
        script_value = ["name", "flowVersion", "inputs", "output"]
        projectId = data.get("common").get("projectId")
        datasets = data.get("datasets", [])
        scripts = data.get("script", {})
        if not isinstance(datasets, list):
            raise Exception('datasets type error')
        if datasets:
            dataset = datasets[-1]
            ds_name = dataset.get("name")
            if query_item("dataset", projectId, "dataset-projectId-name-index", "name", ds_name):
                raise Exception('datasets name already exits')
            self.checkdata(dataset, ds_value)
        if scripts:
            script_name = scripts.get("name")
            runtime = scripts.get("runtime", "")
            if runtime == "dataset":
                self.ds_sc = True
                return

            if [i for i in query_item("dagconf", projectId) if i.get("actionName") == script_name]:
                raise Exception('dagconf actionName already exits')
            self.checkdata(scripts, script_value)
            self.checktype(scripts)

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
    print(event)
    return Check().check_parameter(event)

    # 1. common 必须存在
    # 2. action 必须存在
    # 3. notification 必须存在
    # 4. datasets 和 scripts 必须存在一个
    #   4.1 如果dataset存在，name, cat, format 都必须存在，并判断类型
    #   4.2 如果scripts存在，name, flowVersion, input, output 都必须存在，并判断类型
    #   4.3 如果scripts存在 且存在runtime字段值为 dataset 跳过scripts判断
    # return true
