import json

from util.ExpressionUtil import Expression
from util.Convert2JsonAPI import Convert2JsonAPI
from util.AWS.DynamoDB import DynamoDB
from models.Execution import Execution
from models.Step import Step
from models.Action import Action
from models.DataSet import DataSet
from models.Version import Version
from models.Notification import Notification
from models.Dag import Dag
from models.DagConf import DagConf
from models.Log import Log
from models.Dashboard import Dashboard
from models.Slide import Slide
from models.Scenario import Scenario
from models.ScenarioStep import ScenarioStep
from models.ScenarioTrigger import ScenarioTrigger
from models.Resource import Resource

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
    "batch_get_item": dynamodb.batchGetItem
}

__table_structure = {
    "execution": Execution,
    "step": Step,
    "action": Action,
    "action_dev": Action,
    "dataset": DataSet,
    "notification": Notification,
    "dag": Dag,
    "dagconf": DagConf,
    "logs": Log,
    "dashboard": Dashboard,
    "slide": Slide,
    "version": Version,
    "scenario": Scenario,
    "scenario_step": ScenarioStep,
    "scenario_trigger": ScenarioTrigger,
    "resource": Resource
}


def __queryData(table, body, type_name):
    dy_method = __dynamodb_func[type_name]
    limit = body.get("limit", 100)
    start_key = body.get("start_key", None)
    index_name = body.get("index_name", None)
    if start_key is not None and len(start_key) == 0:
        start_key = None
    conditions = body["conditions"]

    expr = Expression().join_expr(type_name, conditions)
    payload = dy_method({"table_name": table, "index_name": index_name,
                         "limit": limit, "expression": expr, "start_key": start_key})

    result = list(map(lambda item: __table_structure[table](item), payload["data"]))
    json_api_data = json.loads(Convert2JsonAPI(__table_structure[table], many=True).build().dumps(result))
    json_api_data["meta"] = {
        "start_key": payload["start_key"]
    }
    return json_api_data


def __batch_get_items(table, body, type_name):
    dy_method = __dynamodb_func[type_name]
    conditions = body["conditions"]

    expr = Expression().assemble_batch_item_keys(conditions)
    payload = dy_method({"table_name": table, "expression": expr})

    result = list(map(lambda item: __table_structure[table](item), payload["data"]))
    json_api_data = json.loads(Convert2JsonAPI(__table_structure[table], many=True).build().dumps(result))
    return json_api_data


def __putItem(table, body, type_name):
    def ids(items):
        payload = list(map(lambda item: dy_method({"table_name": table, "item": item}), items))
        result = list(map(lambda item: __table_structure[table](item["data"]), payload))
        return json.loads(Convert2JsonAPI(__table_structure[table], many=True).build().dumps(result))

    def base(item):
        payload = dy_method({"table_name": table, "item": item})
        result = __table_structure[table](payload["data"])
        return json.loads(Convert2JsonAPI(__table_structure[table], many=False).build().dumps(result))
    is_ids = {
        "True": ids,
        "False": base
    }
    dy_method = __dynamodb_func[type_name]
    item = body["item"]
    json_api_data = is_ids[str(isinstance(item, list))](item)
    return json_api_data


def __deleteItem(table, body, type_name):
    dy_method = __dynamodb_func[type_name]
    payload = dy_method({"table_name": table, "conditions": body["conditions"]})
    return payload


__exec_func = {
    "query": __queryData,
    "scan": __queryData,
    "put_item": __putItem,
    "delete_item": __deleteItem,
    "batch_get_item": __batch_get_items
}


def makeData(table, body, type_name):
    return __exec_func[type_name](table, body, type_name)
