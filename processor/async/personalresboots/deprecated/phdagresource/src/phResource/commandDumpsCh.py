import json
import requests
from phResource.command import Command
from util.AWS.DynamoDB import DynamoDB
from util.AWS.SNS import SNS



class CommandDumpsCH(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.dynamodb = DynamoDB()
        self.sns = SNS()

    def execute(self):
        # 创建 target group
        # 192.168.16.119
        ip = self.resource_args.get("projectIp")

        topic_arn = "arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phclickhouse-glue-dev"
        message = {
            "project_ip": ip
        }
        self.sns.sns_publish(topic_arn, json.dumps(message, ensure_ascii=False))




