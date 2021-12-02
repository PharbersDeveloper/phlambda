import logging

from util.AWS.DynamoDB import DynamoDB
from delegate.createDagByItem.createDag import CreateDag
from delegate.createDagByItem.createDagConf import CreateDagConf


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt = '%Y-%m-%d  %H:%M:%S %a'
                    )
class Project(object):
    """
        project的父类
    """
    def __init__(self, **kwargs):
        self.dynamodb = DynamoDB()
        self.createDag = CreateDag()
        self.createDagConf = CreateDagConf()
