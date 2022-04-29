import json
import boto3
from boto3.dynamodb.conditions import Attr

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


def scan_table(project_id, ds_name, table_name, item_name):
    try:
        table = dynamodb.Table(table_name)
        result = table.scan(
            FilterExpression=Attr(item_name).eq(ds_name) & Attr("projectId").eq(project_id),
            Limit=10,
        )
        return result.get("Items")
    except:
        return None


def scanTable(self, data):
    table_name = data["table_name"]
    limit = data["limit"]
    expression = data["expression"]
    start_key = data["start_key"]
    table = self.dynamodb_resource.Table(table_name)
    try:
        if len(start_key) == 0:
            result = table.scan(
                FilterExpression=expression,
                Limit=limit,
            )
        else:
            result = table.scan(
                FilterExpression=expression,
                Limit=limit,
                ExclusiveStartKey=start_key
            )
        return {
            "data": result.get("Items"),
            "start_key": result.get("LastEvaluatedKey", "{}")
        }
    except Exception as e:
        print(e)
        return {
            "data": [],
            "start_key": {}
        }


class Check:

    ds_sc = False

    def checkdata(self, data, value):
        if not set(value) <= set(list(data.keys())):
            raise Exception('datasets or scripts Missing field')
        self.ds_sc = True

    def checktype(self, data):
        if data:
            inputs = json.loads(data.get('inputs'))
            output = json.loads(data.get('output'))
            if not isinstance(inputs, list) or not isinstance(output, dict):
                raise Exception('scripts type error')

    def check_datasets_scripts(self, data):
        ds_value = ['cat', 'format', 'name']
        script_value = ["name", "flowVersion", "inputs", "output"]
        projectId = data.get("common").get("projectId")
        datasets = data.get("datasets", [])
        scripts = data.get("scripts", {})
        if not isinstance(datasets, list):
            raise Exception('datasets type error')
        for dataset in datasets:
            ds_name = dataset.get("name")
            if scan_table(projectId, ds_name, "dataset", "name"):
                raise Exception('datasets name already exits')
            self.checkdata(dataset, ds_value)
        if scripts:
            script_name = scripts.get("name")
            if scan_table(projectId, script_name, "dagconf", "actionName"):
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
    return Check().check_parameter(event)

    # 1. common 必须存在
    # 2. action 必须存在
    # 3. notification 必须存在
    # 4. datasets 和 scripts 必须存在一个
    #   4.1 如果dataset存在，name, cat, format 都必须存在，并判断类型
    #   4.2 如果scripts存在，name, flowVersion, input, output 都必须存在，并判断类型
    # return true
