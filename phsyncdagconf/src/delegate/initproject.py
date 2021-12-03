import logging

from util.AWS.DynamoDB import DynamoDB


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
