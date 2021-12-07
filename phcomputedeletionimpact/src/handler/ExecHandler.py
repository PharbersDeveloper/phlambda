import json
from util.AWS.DynamoDB import DynamoDB
from util.ExpressionUtil import Expression

import base64
from util.AWS.STS import STS
from constants.Common import Common
sts = STS().assume_role(
    base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
    "Ph-Back-RW"
)
dynamodb = DynamoDB(sts=sts)
# dynamodb = DynamoDB()


def __convert2obj(item):
    entity = dict({}, **item)
    entity["cmessage"] = json.loads(entity["cmessage"])
    return entity


def __query(table_name, cond):
    return dynamodb.queryTable({
        "table_name": table_name,
        "limit": 1000,
        "expression": cond,
        "start_key": None
    })["data"]


def __ds_query_impact(data):
    def __get_source_job_info(item):
        dag_conf_cond = Expression().join_expr("", {
            "projectId": ["=", data["projectId"]],
            "jobName": ["begins_with", f"""{item["flowVersion"]}_{item["cmessage"]["targetId"]}"""]
        })
        dag_conf_result = __query("dagconf", dag_conf_cond).pop()
        return {
            "projectId": dag_conf_result["projectId"],
            "targetId": dag_conf_result["jobId"],
            "jobName": dag_conf_result["jobName"],
            "type": dag_conf_result["runtime"]
        }

    def __get_target_job_info(item):
        dag_conf_cond = Expression().join_expr("", {
            "projectId": ["=", data["projectId"]],
            "jobName": ["begins_with", f"""{item["flowVersion"]}_{item["cmessage"]["sourceId"]}"""]
        })
        dag_conf_result = __query("dagconf", dag_conf_cond).pop()
        return {
            "projectId": dag_conf_result["projectId"],
            "targetId": dag_conf_result["jobId"],
            "jobName": dag_conf_result["jobName"],
            "type": dag_conf_result["runtime"]
        }

    dag_cond = Expression().join_expr("", {
        "projectId": ["=", data["projectId"]],
        "sortVersion": ["begins_with", data["sortVersion"]]
    })
    dag_result = __query("dag", dag_cond)
    link = list(map(__convert2obj, list(filter(lambda item: item["ctype"] == "link", dag_result))))
    impact_source_link = list(map(__get_source_job_info,
                                  list(filter(lambda item: item["cmessage"]["sourceName"] == data["name"], link))))
    impact_target_link = list(map(__get_target_job_info,
                                  list(filter(lambda item: item["cmessage"]["targetName"] == data["name"], link))))

    return impact_source_link + impact_target_link


def __job_query_impact(data):
    pass


__exec_func = {
    "ds": __ds_query_impact,
    "job": __job_query_impact,
}


def makeData(type_name, data):
    return __exec_func[type_name](data)
