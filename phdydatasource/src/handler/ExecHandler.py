import json
from util.ExpressionUtil import Expression
from util.Convert2JsonAPI import Convert2JsonAPI
from util.AWS.DynamoDB import DynamoDB
from models.Execution import Execution
from models.Step import Step
from models.Action import Action
from models.ProjectFile import ProjectFile
from models.Partition import Partition
from models.DataSet import DataSet
from models.Notification import Notification

# import base64
# from util.AWS.STS import STS
# from constants.Common import Common
# sts = STS().assume_role(
#     base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
#     "Ph-Back-RW"
# )
# dynamodb = DynamoDB(sts=sts)
dynamodb = DynamoDB()

__dynamodb_func = {
    "query": dynamodb.queryTable,
    "scan": dynamodb.scanTable,
    "put_item": dynamodb.putData,
    "delete_item": dynamodb.deleteData,
}

__table_structure = {
    "execution": Execution,
    "step": Step,
    "action": Action,
    "project_files": ProjectFile,
    "partition": Partition,
    "dataset": DataSet,
    "notification": Notification
}


def __queryData(table, body, type_name):
    dy_method = __dynamodb_func[type_name]
    limit = body["limit"]
    start_key = "" if len(body["start_key"]) == 0 else body["start_key"]
    conditions = body["conditions"]

    expr = Expression().join_expr(type_name, conditions)
    payload = dy_method({"table_name": table, "limit": limit, "expression": expr, "start_key": start_key})

    result = list(map(lambda item: __table_structure[table](item), payload["data"]))
    json_api_data = json.loads(Convert2JsonAPI(__table_structure[table], many=True).build().dumps(result))
    json_api_data["meta"] = {
        "start_key": payload["start_key"]
    }
    return json_api_data


def __putItem(table, body, type_name):
    dy_method = __dynamodb_func[type_name]
    payload = dy_method({"table_name": table, "item": body["item"]})
    result = __table_structure[table](payload["data"])
    json_api_data = json.loads(Convert2JsonAPI(__table_structure[table], many=False).build().dumps(result))
    return json_api_data


def __deleteItem(table, body, type_name):
    dy_method = __dynamodb_func[type_name]
    payload = dy_method({"table_name": table, "conditions": body["conditions"]})
    return payload


__exec_func = {
    "query": __queryData,
    "scan": __queryData,
    "put_item": __putItem,
    "delete_item": __deleteItem
}


def makeData(table, body, type_name):
    return __exec_func[type_name](table, body, type_name)


# if __name__ == '__main__':
#     # result = Expression().join_expr("scan", {"name": ["=", "alex"], "id": ["in", ["001", "002"]]})
#     # print(result)
#     import base64
#     from util.AWS.STS import STS
#     from constants.Common import Common
#
#     sts = STS().assume_role(
#         base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
#         "Ph-Back-RW"
#     )
#     dynamodb = DynamoDB(sts=sts)
#     result = dynamodb.scanTable({
#         "table_name": "notification",
#         "limit": 100,
#         "expression":  Expression().join_expr("scan", {"id": ["in", ["3a3fee85d91cfaad226efe98f01c1c9e.xlsx", "d69a88e8bc94a2b67149f2c1a3663f08.xlsx"]]}),
#         "start_key": ""
#     })
#     print(result)
