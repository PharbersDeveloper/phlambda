import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID

class RollBack():

    def __init__(self, **kwargs):
        self.dynamodb = DynamoDB()

    def dag_conf_rollback(self, dag_conf_list):
        for dag_conf in dag_conf_list:
            table_name = "dagconf"
            flowVersion = dag_conf.get("flowVersion")
            jobName = dag_conf.get("jobName")
            data = {
                "table_name": table_name,
                "key": {
                    "flowVersion": flowVersion,
                    "jobName": jobName
                },
            }
            self.dynamodb.delete_item(data)

        return "dag_conf 回滚成功"


    def dag_rollback(self, dag_item_list):
        for dag_item in dag_item_list:
            table_name = dag_item.get("table_name")
            key = {
                "projectId": dag_item["item"].get("projectId"),
                "sortVersion": dag_item["item"].get("sortVersion")
            }
            data = {}
            data["table_name"] = table_name
            data["key"] = key
            self.dynamodb.delete_item(data)

        return "dag 回滚成功"