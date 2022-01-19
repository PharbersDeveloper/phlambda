
from phResource.command import Command
from util.AWS.ELB import ELB
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class CommandRegisterTarget(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.elb = ELB()

    def execute(self):
        # 192.168.16.119

        targets = []
        target = {
            "Id": self.target_ip,
            "Port": 8080
        }
        targets.append(target)
        logger = PhLogging().phLogger("register_target", LOG_DEBUG_LEVEL)
        logger.debug("register_target 流程")

        self.elb.register_targets(self.target_group_arn, targets)
        logger.debug("register_target 完成")