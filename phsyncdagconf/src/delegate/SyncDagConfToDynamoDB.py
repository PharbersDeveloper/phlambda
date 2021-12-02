import os
import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID
from delegate.createDag import CreateDag
from delegate.createDagConf import CreateDagConf
from delegate.updateAction import UpdateAction
from delegate.rollBack import RollBack
from delegate.uploadAirflow import Airflow


# TODO: class 命名用户
class SyncDagConfToDynamoDB:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        # TODO: 这个地方用Facade合适吗？不要靠本能写程序！！！！！
        # 在设计上，需要对以下五个地方进行重构：
        # 1. 不同的project 创建不同的实体，这是典型的工厂，工厂本身是单例，类实例之间的管理还是用单例
        # 2. 同时，创建的流程是一个状态机，每一步的状态机都是一个Command命令设计模式
        #       利用这样的流程可以去掉所有的if与switch，这就是继承和多态的正确用法
        #   2.1 在状态机器上，加入异常的抓取，对每一步的异常形成具体的错误类，对每一个类确定固定的返回值
        #       这种设计模式叫Null Object的变体
        # 3. 最后，如果没有任何异常后，在统一更新数据库，这样你在中间数据出现任何的错误都不会对存储数据产生影响
        #       在没有回滚机制的NoSQL数据库中不能依赖SQL的batch Update机制
        #       也就是需要在编程思想上解决对SQL的依赖，特别是回滚,
        #       同时还需要保证在数据创建失败的情况下，不影响Airflow的原先的dag文件
        # 4. 对这个函数加入一个分布式锁，利用projectId作为自己的钥匙，写到Redis中，保证一次在同一个项目中只能有一个人
        #       能创建job
        # 5. 利用策略模式，把创建所有level的流程，抽离出来，这个部分会长期修改，并可能不由你单人修改
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
            if not json.loads(item.get("message")).get("dagName"):
                status = None

        return status

    def exec(self):
        # 处理event
        item_list = self.process_insert_event()

        if not item_list:
            # TODO: 不要是用print，用logger代替
            print("操作不是INSERT")
        else:
            status = self.insert_action(item_list)
            if status:
                for item in item_list:
                    if json.loads(item.get("message")).get("dagName"):
                        try:
                            # 插入dagconf信息
                            dag_conf = self.createDagConf.insert_dagconf(item)
                        except Exception as e:
                            # TODO 此处添加回滚功能
                            # 对已经插入的item 进行回滚
                            # self.rollBack.dag_conf_rollback(dag_conf_list)
                            status = "插入dag_conf时错误:" + json.dumps(str(e), ensure_ascii=False)
                            raise Exception(status)
                        else:
                            # 更新action 中job cat为 dag_conf insert success
                            status = "dag_conf insert success"
                        finally:
                            # 更新action 信息
                            self.updateAction.updateItem(item, "action", status)
                            if not status == "dag_conf insert success":
                                self.updateAction.updateNotification(item, "notification", dag_conf={}, status=status)
                            else:
                                self.updateAction.updateNotification(item, "notification", dag_conf, status)

                        try:
                            # 插入dag信息
                            dag_item = self.createDag.create_dag(dag_conf)
                        except Exception as e:
                            # TODO 此处添加回滚功能
                            # self.rollBack.dag_rollback(dag_item_list)
                            status = "插入dag时错误:" + json.dumps(str(e), ensure_ascii=False)
                            raise Exception(status)
                        else:
                            # 更新action 中job cat为 dag insert success
                            status = "dag insert success"
                        finally:
                            # 插入dag成功后更新action 信息
                            self.updateAction.updateItem(item, "action", status)
                            if not status == "dag insert success":
                                self.updateAction.updateNotification(item, "notification", dag_conf={}, status=status)
                            else:
                                self.updateAction.updateNotification(item, "notification", dag_conf, status)

            else:
                print("不符合dag规范的action")

        airflow_item_list = self.process_insert_event()
        # 创建airflow相关文件
        try:
            self.airflow.airflow(airflow_item_list)
        except Exception as e:
            status = "创建airflow相关文件时错误:" + json.dumps(str(e), ensure_ascii=False)
            raise Exception(status)
        else:
            # 更新action 中job cat为 dag_conf insert success
            status = "airflow job create success"
        finally:
            for item in item_list:
                self.updateAction.updateItem(item, "action", status)
                self.updateAction.updateNotification(item, "notification", dag_conf={}, status=status)



if __name__ == '__main__':
    with open("../events/event_a.json") as f:
        event = json.load(f)
    app = SyncDagConfToDynamoDB(event=event)
    app.exec()
