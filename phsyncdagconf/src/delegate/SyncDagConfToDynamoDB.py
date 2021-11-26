import os
import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID
from delegate.createDag import CreateDag
from delegate.createDagConf import CreateDagConf
from delegate.updateAction import UpdateAction
from delegate.rollBack import RollBack
from delegate.uploadAirflow import Airflow

class SyncDagConfToDynamoDB:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.dynamodb = DynamoDB()
        self.createDag = CreateDag()
        self.createDagConf = CreateDagConf()
        self.updateAction = UpdateAction()
        self.rollBack = RollBack()
        self.airflow = Airflow()

    def process_insert_event(self):
        # 获取新插入item的 partition_key, sort_key, message
        item_list = []
        records = self.event.get("Records")
        for record in records:
            if record.get("eventName") == "INSERT":
                new_image = record["dynamodb"]["NewImage"]
                item = {}
                for item_key in list(new_image.keys()):
                    value = new_image[item_key]
                    item_value = list(value.keys())[0]
                    item[item_key] = value[item_value]
                item_list.append(item)
        return item_list


    def exec(self):
        # 处理event
        item_list = self.process_insert_event()

        try:
            # 插入dagconf信息
            dag_conf_list = self.createDagConf.insert_dagconf(item_list)
            print(dag_conf_list)
            self.airflow.airflow(dag_conf_list)
        except Exception as e:
            # TODO 此处添加回滚功能
            # 对已经插入的item 进行回滚
            self.rollBack.dag_conf_rollback(dag_conf_list)
            raise Exception("插入dag_conf时错误:" + json.dumps(str(e)))
        else:
            # 更新action 中job cat为 dag_conf insert success
            status = "dag_conf insert success"
            # 插入dag_conf 成功后更新action 信息
            self.updateAction.updateItem(item_list, "action", status)
            self.updateAction.updateItem(item_list, "notification", status)
        try:
            # 插入dag信息
            dag_item_list = self.createDag.create_dag(dag_conf_list)
        except Exception as e:
            # TODO 此处添加回滚功能
            # self.rollBack.dag_rollback(dag_item_list)
            raise Exception("插入dag时错误:" + json.dumps(str(e)))
        else:
            # 更新action 中job cat为 dag insert success
            status = "dag insert success"
            # 插入dag成功后更新action 信息
            self.updateAction.updateItem(item_list, "action", status)
            self.updateAction.updateItem(item_list, "notification", status)


if __name__ == '__main__':
    with open("../events/event_a.json") as f:
        event = json.load(f)
    app = SyncDagConfToDynamoDB(event=event)
    app.exec()
