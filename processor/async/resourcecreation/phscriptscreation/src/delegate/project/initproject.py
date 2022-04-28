import logging

from util.AWS.DynamoDB import DynamoDB
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class Project(object):
    """
        project的父类
    """
    def __init__(self, **kwargs):
        self.dynamodb = DynamoDB()

    def exec(self):
        pass


