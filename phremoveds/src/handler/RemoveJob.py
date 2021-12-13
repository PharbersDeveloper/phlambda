import json
import time
from boto3.dynamodb.conditions import Key, Attr


class RemoveJob:
    def __init__(self, dynamodb):
        self.dynamodb = dynamodb

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
    def removeJob2S3(self, path):
        pass

    def removeJob(self, id, projectId, jobName, owner, showName):
        dag_job_result = self.dynamodb.scanTable({
            "table_name": "dag",
            "expression": Key("projectId").eq(projectId) & Key("representId").eq(id),
            "limit": 1000,
            "start_key": ""
        })["data"]
        if len(dag_job_result) > 0:
            dag_link_result = self.dynamodb.scanTable({
                "table_name": "dag",
                "expression": Attr("projectId").eq(projectId) & Attr("ctype").eq("link"),
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
                        "projectId": projectId,
                        "sortVersion": item["sortVersion"]
                    }
                })

            self.dynamodb.deleteData({
                "table_name": "dag",
                "conditions": {
                    "projectId": projectId,
                    "sortVersion": dag_job_result[0]["sortVersion"]
                }
            })

        dag_conf_result = self.dynamodb.queryTable({
            "table_name": "dagconf",
            "expression": Key("projectId").eq(projectId) & Key("jobName").eq(jobName),
            "limit": 1000,
            "start_key": ""
        })["data"]

        dag_conf_results = self.dynamodb.scanTable({
            "table_name": "dagconf",
            "expression": Attr("projectId").eq(projectId) & Attr("flowVersion").eq("developer"),
            "limit": 10000,
            "start_key": ""
        })["data"]

        dag_conf_results = list(map(self.__convert2dag_conf, dag_conf_results))

        # def diff(data):
        #     outputs = set(map(lambda ds: ds["id"], json.loads(dag_conf_result[0]["outputs"])))
        #     inputs = set(map(lambda ds: ds["id"], data["inputs"]))
        #     return len(outputs & inputs) > 0

        target_result = list(filter(lambda data: dag_conf_result[0]["jobId"] in data["targetJobId"], dag_conf_results))
        # input_result = list(filter(diff, dag_conf_results))

        for item in target_result:
            targetJobId = list(filter(lambda data: dag_conf_result[0]["jobId"] != data, item["targetJobId"]))
            item["targetJobId"] = targetJobId

        # for item in input_result:
        #     cur_output_ids = set(map(lambda output: output["id"], json.loads(dag_conf_result[0]["outputs"])))
        #     for id in cur_output_ids:
        #         item["inputs"] = list(filter(lambda input: input["id"] != id, item["inputs"]))

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
                "projectId": projectId,
                "jobName": jobName
            }
        })
        self.dynamodb.putData({
            "table_name": "action",
            "item": {
                "projectId": projectId,
                "code": 0,
                "comments": "dag_refresh",
                "date": int(round(time.time() * 1000)),
                "jobCat": "dag_refresh",
                "jobDesc": "refresh",
                "message": json.dumps({
                    "projectId": projectId,
                    "jobName": jobName,
                    "flowVersion": dag_conf_result[0]["flowVersion"] if len(dag_conf_result) > 0 else "developer",
                    "jobCat": "dag_refresh"
                }),
                "owner": owner,
                "showName": showName
            }
        })
        return 1

    def exec(self, item, message):
        return self.removeJob(message["targetId"], item["projectId"], message["jobName"], item["owner"], item["showName"])
