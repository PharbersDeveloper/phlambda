
from phResource.command import Command
from util.AWS.ELB import ELB

from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL

class CommandCreateTargetGroup(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.elb = ELB()

    def execute(self):
        # 创建 target group
        # 192.168.16.119
        logger = PhLogging().phLogger("creat_target_group", LOG_DEBUG_LEVEL)
        logger.debug("target_group 创建流程")

        target_port = 8080
        target_group_arn = self.elb.create_target_group(self.target_name, target_port)

        logger.debug("target_group 创建完成")
        return target_group_arn
