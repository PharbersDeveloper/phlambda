

from delegate.createDagByItem.createDag import CreateDag
from delegate.createDagByItem.createDagConf import CreateDagConf
from delegate.createDagByItem.uploadAirflow import Airflow
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt='%Y-%m-%d  %H:%M:%S %a'
                    )


class Order:

    def run(self):
        pass


class CreateDagOrder(Order):
    def __init__(self, **kwargs):
        self.dag_conf = kwargs.get("dag_conf")
        pass

    def run(self):
        CreateDag.exec(self, self.dag_conf)


class CreateDagConfOrder(Order):
    def __init__(self, **kwargs):
        self.dag_conf = kwargs.get("dag_conf")
        pass

    def run(self):
        CreateDagConf.exec(self, self.dag_conf)


class CreateAirflowFileOrder(Order):
    def __init__(self, **kwargs):
        self.dag_conf = kwargs.get("dag_conf")
        pass

    def run(self):
        Airflow.exec(self, self.dag_conf)


class Agent:
    def __init__(self):
        self.__orderQueue = []

    def place_order(self, order):
        self.__orderQueue.append(order)
        order.run()


def exec(item_order_list, dag_conf):

    item_map = {
        "createDag": CreateDagOrder(dag_conf=dag_conf),
        "createDagConf": CreateDagConfOrder(dag_conf=dag_conf),
        "createAirflowFile": CreateAirflowFileOrder(dag_conf=dag_conf),
    }

    # 调用
    agent = Agent()
    for item_order in item_order_list:
        agent.place_order(item_map[item_order])