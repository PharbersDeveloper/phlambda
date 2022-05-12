import json
import logging

from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL
from util.AWS.SQS import SQS


class ForwardEvent(object):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.sqs = SQS()

    def execute(self):
        print(self.event)
        print("开始发送 消息")
        self.sqs.sqs_send_message(self.event)
        print("send message success")


