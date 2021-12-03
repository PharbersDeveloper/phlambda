
from delegate.createDagByItem.command import Command
from delegate.createDagByItem.commandCreateDag import CommandCreateDag
from delegate.createDagByItem.commandCreateDagConf import CommandCreateDagConf
from delegate.createDagByItem.commandUploadAirflow import CommandUploadAirflow
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


def exec(dag_item):

    # 创建dag_conf 返回dag_conf_data
    dag_conf_data = CommandCreateDagConf(dag_item=dag_item).run()
    logging.info("创建写入dag_conf数据库数据成功")
    logging.info(dag_conf_data)

    # 创建dag 返回dag_data
    dag_data = CommandCreateDag(dag_conf=dag_conf_data.get("item")).run()
    # logging.info("创建写入dag数据库数据成功")
    # logging.info(dag_data)

    # 创建airflow 返回airflow_data

    return dag_conf_data

