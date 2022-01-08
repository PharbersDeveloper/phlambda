import json

from delegate.createDagByItem.command import Command
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt='%Y-%m-%d  %H:%M:%S %a'
                    )


class CommandPutItemToDB(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.dynamodb = DynamoDB()

    def put_item_to_dag(self, dag_item_list):
        for dag_item in dag_item_list:
            dag_item_data = {
                "table_name": "dag",
                "item": dag_item
            }
            self.dynamodb.putData(dag_item_data)


    def put_item_to_dag_conf(self, dag_conf_list):

        for dag_conf_item in dag_conf_list:
            dag_conf_item_data = {
                "table_name": "dagconf",
                "item": dag_conf_item
            }
            self.dynamodb.putData(dag_conf_item_data)

    def del_same_dag_conf_item(self):


        projectId = self.dag_conf_list[0].get("projectId")
        query_data = {
            "table_name": "dagconf",
            "partition_key": "projectId",
            "partition_value": projectId,
            "sort_key": "jobName",
            "sort_value": "developer"
        }
        delete_data = {
            "table_name": "dagconf",
            "partitionKey": "projectId",
            "sortKey": "jobName"
        }
        self.dynamodb.delete_dag_conf_item_by_partitionkey_sortkey(query_data, delete_data)

    def del_same_dag_item(self, dag_conf_outputs):

        projectId = self.dag_conf_list[0].get("projectId")
        query_data = {
            "table_name": "dag",
            "partition_key": "projectId",
            "partition_value": projectId,
            "sort_key": "sortVersion",
            "sort_value": "developer"
        }
        delete_data = {
            "table_name": "dag",
            "partitionKey": "projectId",
            "sortKey": "sortVersion"
        }
        self.dynamodb.delete_dag_item_by_partitionkey_sortkey(query_data, delete_data, dag_conf_outputs)

    def get_all_dag_conf_output(self):
        output_ids = []
        for dag_conf in self.dag_conf_list:
            id = eval(dag_conf.get("outputs"))[0].get("id")
            output_ids.append(id)
        return output_ids

    def run(self):

        # 处理所有dag_conf的output
        dag_conf_output_ids = self.get_all_dag_conf_output()

        # 先进行删除 根据 projectId flowVersion
        self.del_same_dag_conf_item()
        self.del_same_dag_item(dag_conf_output_ids)
        # # 上传item 到dag_conf
        self.put_item_to_dag_conf(self.dag_conf_list)
        # 上传item 到dag
        self.put_item_to_dag(self.dag_item_list)

