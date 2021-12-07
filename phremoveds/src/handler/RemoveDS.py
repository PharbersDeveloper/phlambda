import json
import http.client
import urllib.parse
from boto3.dynamodb.conditions import Attr


class RemoveDS:
    def __init__(self, dynamodb):
        self.dynamodb = dynamodb

    def __convert2obj(self, item):
        entity = dict({}, **item)
        entity["cmessage"] = json.loads(entity["cmessage"])
        return entity

    def executeSql(self, sql, type):
        conn = http.client.HTTPConnection(host="192.168.16.117", port="8123")
        url = urllib.parse.quote("/ch/?query=" + sql, safe=':/?=&')
        conn.request(type, url)
        res = conn.getresponse()
        return res.read().decode("utf-8")

    def removeClickHouseData(self, tableName):
        sql = "DROP TABLE `{0}`".format(tableName)
        result = self.executeSql(sql, "POST")
        return 0 if result else 1

    def removeDynamoDBData(self, tableName, id, projectId):
        dag_ds_result = self.dynamodb.scanTable({
            "table_name": "dag",
            "expression": Attr("projectId").eq(projectId) & Attr("representId").eq(id),
            "limit": 1000,
            "start_key": ""
        })["data"].pop()

        dag_link_result = self.dynamodb.scanTable({
            "table_name": "dag",
            "expression": Attr("projectId").eq(projectId) & Attr("cat").eq("null"),
            "limit": 1000,
            "start_key": ""
        })["data"]

        link = list(map(self.__convert2obj, dag_link_result))
        impact_link = list(filter(lambda item: item["cmessage"]["sourceName"] == dag_ds_result["name"], link)) + \
                      list(filter(lambda item: item["cmessage"]["targetName"] == dag_ds_result["name"], link))

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
                "sortVersion": dag_ds_result["sortVersion"]
            }
        })

        self.dynamodb.deleteData({
            "table_name": tableName,
            "conditions": {
                "id": id,
                "projectId": projectId,
            }
        })
        return 1

    def exec(self, item, message):
        return self.removeClickHouseData(item["projectId"] + "_" + message["destination"]) & \
               self.removeDynamoDBData("dataset", message["dsid"], item["projectId"])
