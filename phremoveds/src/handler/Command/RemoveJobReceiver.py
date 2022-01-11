import json
import constants.Common as Common
from handler.Command.Receiver import Receiver
from boto3.dynamodb.conditions import Key, Attr
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL


class RemoveJobReceiver(Receiver):

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]
        self.logger = PhLogging().phLogger("Remove Job", LOG_DEBUG_LEVEL)


    def __convert2obj(self, item):
        entity = dict({}, **item)
        entity["cmessage"] = json.loads(entity["cmessage"])
        return entity

    def __convert2dag_conf(self, item):
        entity = dict({}, **item)
        entity["targetJobId"] = json.loads(entity["targetJobId"])
        entity["outputs"] = json.loads(entity["outputs"])
        entity["inputs"] = json.loads(entity["inputs"])
        return entity

    # TODO 删除s3脚本没做
    def __removeJob2S3(self, path):
        pass

    def exec(self, data):
        self.logger.debug(f"{data}")
        project_id = data["project_id"]
        target_id = data["target_id"]
        job_name = data["job_name"]
        flow_version = data["flow_version"]

        dag_job_result = self.dynamodb.scanTable({
            "table_name": "dag",
            "expression": Key("projectId").eq(project_id) & Key("representId").eq(target_id),
            "limit": 1000,
            "start_key": ""
        })["data"]
        if len(dag_job_result) > 0:
            dag_link_result = self.dynamodb.scanTable({
                "table_name": "dag",
                "expression": Attr("projectId").eq(project_id) & Attr("ctype").eq("link"),
                "limit": 1000,
                "start_key": ""
            })["data"]

            link = list(map(self.__convert2obj, dag_link_result))
            impact_link = \
                list(filter(lambda item: item["cmessage"]["sourceName"] == dag_job_result[0]["name"], link)) + \
                list(filter(lambda item: item["cmessage"]["targetName"] == dag_job_result[0]["name"], link))
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
                    "sortVersion": dag_job_result[0]["sortVersion"]
                }
            })

        dag_conf_result = self.dynamodb.queryTable({
            "table_name": "dagconf",
            "expression": Key("projectId").eq(project_id) & Key("jobName").eq(job_name),
            "limit": 1000,
            "start_key": ""
        })["data"]

        dag_conf_results = self.dynamodb.scanTable({
            "table_name": "dagconf",
            "expression": Attr("projectId").eq(project_id) & Attr("flowVersion").eq(flow_version),
            "limit": 10000,
            "start_key": ""
        })["data"]

        dag_conf_results = list(map(self.__convert2dag_conf, dag_conf_results))

        target_result = list(filter(lambda data: dag_conf_result[0]["jobId"] in data["targetJobId"], dag_conf_results))

        for item in target_result:
            targetJobId = list(filter(lambda data: dag_conf_result[0]["jobId"] != data, item["targetJobId"]))
            item["targetJobId"] = targetJobId

        for item in dag_conf_results:
            item["targetJobId"] = json.dumps(item["targetJobId"])
            item["inputs"] = json.dumps(item["inputs"])
            item["outputs"] = json.dumps(item["outputs"])
            self.dynamodb.putData({
                "table_name": "dagconf",
                "item": item
            })

        self.dynamodb.deleteData({
            "table_name": "dagconf",
            "conditions": {
                "projectId": project_id,
                "jobName": job_name
            }
        })
