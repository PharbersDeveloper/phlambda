
from phResource.command import Command
from util.AWS.DynamoDB import DynamoDB
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL
from util.GenerateID import GenerateID


class CommandPutNotification(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.dynamodb = DynamoDB()

    def execute(self):
        # 创建 target group
        # 192.168.16.119
        logger = PhLogging().phLogger("put_resource_args", LOG_DEBUG_LEVEL)
        logger.debug("resource_args 创建流程")
        data = {
            "table_name": "resource"
        }
        item = {}
        message = {}
        message.update({"projectIp": self.target_ip})
        message.update({"ruleArn": self.rule_arn})
        message.update({"targetGroupArn": self.target_group_arn})
        message.update({"projectName": self.target_name})

        item.update({"id": self.action_id})
        item.update({"projectId": self.project_id})
        item.update({"code": "0"})
        item.update({"showName": ""})
        item.update({"jobDesc": ""})
        item.update({"commnets": ""})
        item.update({"owner": ""})
        item.update({"message": message})
        item.update({"jobCat": "create success"})

        data.update({"item": item})
        self.dynamodb.putData(data)
        logger.debug("resource_args 创建完成")
