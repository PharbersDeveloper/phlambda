import os
import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID
from delegate.createDag import CreateDag
from delegate.createDagConf import CreateDagConf
from delegate.updateAction import UpdateAction
from delegate.rollBack import RollBack
from delegate.level import DagLevel
from delegate.uploadAirflow import Airflow
from delegate.putItemToDy import PutItemToDy

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

    def insert_action(self, item_list):
        status = "dag_action"
        for item in item_list:
            if not json.loads(item.get("message")).get("flowVersion"):
                status = None

        return status

    def exec(self):
        # 处理event
        item_list = self.process_insert_event()
        if not item_list:
            print("操作不是INSERT")
        else:
            status = self.insert_action(item_list)
            if status:
                for item in item_list:
                    if json.loads(item.get("message")).get("dagName"):
                        try:
                            # 插入dagconf信息
                            dag_conf_list = self.createDagConf.insert_dagconf(item)
                            create_level = DagLevel(dag_conf_list=dag_conf_list)
                            dag_item_list = create_level.exec()
                        except Exception as e:
                            status = "创建dag_conf时错误:" + json.dumps(str(e), ensure_ascii=False)
                            self.updateAction.updateNotification(item, "notification", dag_conf={}, status=status)
                        else:
                            # 更新action 中job cat为 dag_conf insert success
                            status = "dag_conf insert success"
                            pass
                        try:
                            # 创建dag_item_list
                            dag_item_list = self.createDag.create_dag(dag_item_list, dag_conf_list)
                        except Exception as e:
                            status = "创建dag时错误:" + json.dumps(str(e), ensure_ascii=False)
                            self.updateAction.updateNotification(item, "notification", dag_conf={}, status=status)
                        else:
                            # 更新action 中job cat为 dag insert success
                            status = "dag insert success"
                            pass

                        # try:
                        #     # 插入dag信息
                        #     putItem = PutItemToDy(dag_conf_list=dag_conf_list, dag_item_list=dag_item_list)
                        #     putItem.put_dag_job()
                        # except Exception as e:
                        #     status = "将dag上传时错误:" + json.dumps(str(e), ensure_ascii=False)
                        #     self.updateAction.updateNotification(item, "notification", dag_conf={}, status=status)
                        #     raise e
                        # else:
                        #     # 更新action 中job cat为 dag insert success
                        #     status = "dag insert success"
                        #     pass

                    elif item.get("jobCat") == "dag_refresh":
                        try:
                            dag_conf_list = self.createDagConf.refresh_dagconf(item)
                            create_level = DagLevel(dag_conf_list=dag_conf_list)
                            dag_item_list = create_level.exec()
                        except Exception as e:
                            status = "创建dag_conf时错误:" + json.dumps(str(e), ensure_ascii=False)
                            self.updateAction.updateNotification(item, "notification", dag_conf={}, status=status)
                        else:
                            # 更新action 中job cat为 dag_conf insert success
                            # status = "dag_conf insert success"
                            pass
                        try:
                            dag_item_list = self.createDag.create_dag(dag_item_list, dag_conf_list)
                        except Exception as e:
                            status = "创建dag时错误:" + json.dumps(str(e), ensure_ascii=False)
                            self.updateAction.updateNotification(item, "notification", dag_conf={}, status=status)
                        else:
                            # 更新action 中job cat为 dag insert success
                            status = "daginsert success"
                            pass

                        try:
                            # 插入dag信息
                            putItem = PutItemToDy(dag_conf_list=dag_conf_list, dag_item_list=dag_item_list)
                            putItem.put_dag_job()
                        except Exception as e:
                            status = "将dag上传时错误:" + json.dumps(str(e), ensure_ascii=False)
                            self.updateAction.updateNotification(item, "notification", dag_conf={}, status=status)
                        else:
                            # 更新action 中job cat为 dag insert success
                            status = "dag insert success"
                            pass
                    
            else:
                print("不符合dag规范的action")

        airflow_item_list = self.process_insert_event()
        if json.loads(airflow_item_list[0].get("message")).get("dagName") or airflow_item_list[0].get("jobCat") == "dag_refresh":
            # 创建airflow相关文件
            try:
                pass
                self.airflow.airflow(airflow_item_list)
            except Exception as e:
                status = "创建airflow相关文件时错误:" + json.dumps(str(e), ensure_ascii=False)
            else:
                # 更新action 中job cat为 dag_conf insert success2
                status = "dag insert success"
            # finally:
            #
            #     for item in item_list:
            #         dag_conf = {}
            #         for dag_conf_item in dag_conf_list:
            #             if json.loads(item.get("message")).get("jobName") in dag_conf_item.get("jobName"):
            #                 dag_conf = dag_conf_item
            #         self.updateAction.updateItem(item, "action", status)
            #         self.updateAction.updateNotification(item, "notification", dag_conf=dag_conf, status=status)



if __name__ == '__main__':
    with open("../events/event_b.json") as f:
        event = json.load(f)
    app = SyncDagConfToDynamoDB(event=event)
    app.exec()
