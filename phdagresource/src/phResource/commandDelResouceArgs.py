
from phResource.command import Command
from util.AWS.DynamoDB import DynamoDB
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class CommandDelResourceArgs(Command):


    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.dynamodb = DynamoDB()

    def execute(self):
        # 创建 target group
        # 192.168.16.119
        logger = PhLogging().phLogger("put_resource_args", LOG_DEBUG_LEVEL)
        logger.debug("resource_args 删除流程")
        data = {
            "table_name": "resource"
        }
        key = {}
        key.update({"projectName": self.project_name})
        key.update({"projectId": self.project_id})
        data.update({"key": key})
        self.dynamodb.delete_item(data)
        logger.debug("resource_args 删除完成")

