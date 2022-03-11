
from phResource.command import Command
from util.AWS.DynamoDB import DynamoDB
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class CommandGetResourceArgs(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.dynamodb = DynamoDB()

    def execute(self):
        # 创建 target group
        # 192.168.16.119
        logger = PhLogging().phLogger("put_resource_args", LOG_DEBUG_LEVEL)
        logger.debug("从 dynamodb 获取 resource_args 流程")
        data = {
            "table_name": "resource"
        }
        key = {
            "projectId": self.project_id,
            "projectName": self.project_name
        }
        data.update({"key": key})
        resource_args = self.dynamodb.getItem(data)

        logger.debug(resource_args.get("Item"))
        logger.debug("从 dynamodb 获取 resource_args 完成")

        return resource_args.get("Item")
