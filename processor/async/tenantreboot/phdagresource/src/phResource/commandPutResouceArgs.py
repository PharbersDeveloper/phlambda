
from phResource.command import Command
from util.AWS.DynamoDB import DynamoDB
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class CommandPutResourceArgs(Command):

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
        item.update({"projectName": self.target_name})
        item.update({"projectId": self.project_id})
        item.update({"projectIp": self.target_ip})
        data.update({"item": item})
        self.dynamodb.putData(data)
        logger.debug("resource_args 创建完成")
