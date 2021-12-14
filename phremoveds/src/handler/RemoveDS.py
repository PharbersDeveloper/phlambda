import os
import json
import time
import http.client
import urllib.parse
from boto3.dynamodb.conditions import Attr
from constants.Common import Common
from util.PhRedis import PhRedis
from constants.Errors import Errors, ResourceBusy


class RemoveDS:
    def __init__(self, dynamodb):
        self.dynamodb = dynamodb
        self.redis = PhRedis(host=os.environ[Common.REDIS_HOST], port=os.environ[Common.REDIS_PORT]).getRedis()

    def __convert2obj(self, item):
        entity = dict({}, **item)
        entity["cmessage"] = json.loads(entity["cmessage"])
        return entity

    def executeSql(self, sql, type):
        conn = http.client.HTTPConnection(host=os.environ[Common.CLICKHOUSE_HOST],
                                          port=os.environ[Common.CLICKHOUSE_PORT])
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
        })["data"]
        if len(dag_ds_result) > 0:
            dag_link_result = self.dynamodb.scanTable({
                "table_name": "dag",
                "expression": Attr("projectId").eq(projectId) & Attr("ctype").eq("link"),
                "limit": 1000,
                "start_key": ""
            })["data"]

            link = list(map(self.__convert2obj, dag_link_result))
            impact_link = list(filter(lambda item: item["cmessage"]["sourceName"] == dag_ds_result[0]["name"], link)) + \
                          list(filter(lambda item: item["cmessage"]["targetName"] == dag_ds_result[0]["name"], link))

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
                    "sortVersion": dag_ds_result[0]["sortVersion"]
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
        check_key = os.environ[Common.CHECK_APP_NAME] + "_" + item["projectId"] + "_" + message["destination"]
        set_key = os.environ[Common.LOCK_APP_NAME] + "_" + item["projectId"] + "_" + message["destination"]
        try:
            if self.redis.exists(check_key):
                raise ResourceBusy("Resources Are Busy")
            else:
                if self.redis.setnx(set_key, int(round(time.time() * 1000))):
                    self.redis.expire(set_key, 60)

                # result = 1
                result = self.removeClickHouseData(item["projectId"] + "_" + message["destination"]) & \
                         self.removeDynamoDBData("dataset", message["dsid"], item["projectId"])

                return result
        except ResourceBusy as e:
            raise e
        except Exception as e:
            raise Errors(e)
        finally:
            self.redis.delete(set_key)
