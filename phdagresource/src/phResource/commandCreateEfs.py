import json
import subprocess
import os

from phResource.command import Command
from util.AWS.SNS import SNS


class CommandCreateEfs(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.sns = SNS()

    def create_dir(self):
        # 发送sns消息到  sns topic ph_dag_resource
        topic_arn = "arn:aws-cn:sns:cn-northwest-1:444603803904:ph_dag_resource"
        message = {
            "project_name": self.target_name,
            "operator_type": "create"
        }
        self.sns.sns_publish(topic_arn, json.dumps(message, ensure_ascii=False))

    def execute(self):
        # 192.168.16.119

        self.create_dir()

        pass
