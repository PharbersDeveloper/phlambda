
from delegate.createDagByItem.command import Command
from delegate.createDagByItem.commandCreateDag import CommandCreateDag
from delegate.createDagByItem.commandCreateDagConf import CommandCreateDagConf
from delegate.createDagByItem.commandUploadAirflow import CommandUploadAirflow
from delegate.createDagByItem.commandPutItemToDB import CommandPutItemToDB
from delegate.createDagByItem.commandCreateDagLevel import CommandCreateDagLevel
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt='%Y-%m-%d  %H:%M:%S %a'
                    )


# class CreateDagCommand(Command):
#     def __init__(self, **kwargs):
#         self.dag_item = kwargs.get("dag_item")
#         self.create_dag = CreateDag(dag_item=self.dag_item)
#         pass
#
#     def run(self):
#         return self.create_dag.exec()
#
#
# class CreateDagConfCommand(Command):
#     def __init__(self, **kwargs):
#         self.dag_item = kwargs.get("dag_item")
#         self.create_dag_conf = CreateDagConf(dag_item=self.dag_item)
#         pass
#
#     def run(self):
#         return self.create_dag_conf.exec()
#
#
# class CreateAirflowFileCommand(Command):
#     def __init__(self, **kwargs):
#         self.dag_item = kwargs.get("dag_item")
#         self.create_airflow_file = Airflow(dag_item=self.dag_item)
#         pass
#
#     def run(self):
#         self.create_airflow_file.exec()


# class Agent:
#     def __init__(self):
#         self.__commandQueue = []
#
#     def place_command(self, command):
#         self.__commandQueue.append(command)
#         data = command.run()
#         return data


def max_exec(dag_item):

    # 创建dag_conf 返回dag_conf_data
    dag_conf_list = CommandCreateDagConf(dag_item=dag_item).run()
    logging.info("创建dag_conf成功")
    logging.info(dag_conf_list)

    # 根据dag_conf_list 创建 Level并返回 dag_item_level_list
    level_type = "SCRIPT_LEVEL"
    dag_item_level_list = CommandCreateDagLevel(dag_conf_list=dag_conf_list, level_type=level_type).run()

    # 创建dag 返回dag_data
    dag_item_list = CommandCreateDag(dag_conf_list=dag_conf_list, dag_item_level_list=dag_item_level_list).run()

    # 将创建好的dag上传到dynamodb
    putItem = CommandPutItemToDB(dag_conf_list=dag_conf_list, dag_item_list=dag_item_list).run()

    # 创建airflow 返回airflow_data

    return {}

