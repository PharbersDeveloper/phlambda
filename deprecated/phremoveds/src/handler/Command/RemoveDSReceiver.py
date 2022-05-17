import json
import constants.Common as Common
from handler.Command.Receiver import Receiver
from boto3.dynamodb.conditions import Attr
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL


class RemoveDSReceiver(Receiver):

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]
        self.logger = PhLogging().phLogger("Remove DS", LOG_DEBUG_LEVEL)

    def __convert2obj(self, item):
        entity = dict({}, **item)
        entity["cmessage"] = json.loads(entity["cmessage"])
        return entity

    def exec(self, data):
        self.logger.debug(f"{data}")
        ds_id = data["message"]["dsid"]
        project_id = data["projectId"]
        dag_ds_result = self.dynamodb.scanTable({
            "table_name": "dag",
            "expression": Attr("projectId").eq(project_id) & Attr("representId").eq(ds_id),
            "limit": 100000000,
            "start_key": ""
        })["data"]
        if len(dag_ds_result) > 0:
            dag_link_result = self.dynamodb.scanTable({
                "table_name": "dag",
                "expression": Attr("projectId").eq(project_id) & Attr("ctype").eq("link"),
                "limit": 100000000,
                "start_key": ""
            })["data"]

            link = list(map(self.__convert2obj, dag_link_result))
            impact_link = list(filter(lambda item: item["cmessage"]["sourceName"] == dag_ds_result[0]["name"], link)) + \
                          list(filter(lambda item: item["cmessage"]["targetName"] == dag_ds_result[0]["name"], link))

            for item in impact_link:
                self.dynamodb.deleteData({
                    "table_name": "dag",
                    "conditions": {
                        "projectId": project_id,
                        "sortVersion": item["sortVersion"]
                    }
                })

            self.dynamodb.deleteData({
                "table_name": "dag",
                "conditions": {
                    "projectId": project_id,
                    "sortVersion": dag_ds_result[0]["sortVersion"]
                }
            })

        self.dynamodb.deleteData({
            "table_name": "dataset",
            "conditions": {
                "id": ds_id,
                "projectId": project_id,
            }
        })
