import json
from boto3.dynamodb.conditions import Key, Attr


class RemoveJob:
    def __init__(self, dynamodb):
        self.dynamodb = dynamodb

    def __convert2obj(self, item):
        entity = dict({}, **item)
        entity["cmessage"] = json.loads(entity["cmessage"])
        return entity

    # TODO 删除s3脚本没做
    def removeJob2S3(self, path):
        pass

    def removeJob(self, id, projectId, jobName):
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
            impact_link = list(filter(lambda item: item["cmessage"]["sourceName"] == dag_job_result[0]["name"], link)) + \
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

        self.dynamodb.deleteData({
            "table_name": "dagconf",
            "conditions": {
                "projectId": projectId,
                "jobName": jobName
            }
        })
        return 1

    def exec(self, item, message):
        return self.removeJob(message["targetId"], item["projectId"], message["jobName"])
