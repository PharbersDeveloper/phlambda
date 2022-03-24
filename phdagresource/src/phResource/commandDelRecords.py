
from phResource.command import Command
from util.AWS.ROUTE53 import ROUTE53
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class CommandDelRecords(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.route53 = ROUTE53()

    def execute(self):
        # 192.168.16.119
        logger = PhLogging().phLogger("delete_records", LOG_DEBUG_LEVEL)
        logger.debug("records 删除流程")

        self.route53.delete_records(self.target_name)

        logger.debug("records 删除成功")
