
from phResource.command import Command
from util.AWS.ELB import ELB
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class CommandDelRule(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.elb = ELB()

    def execute(self):
        # 192.168.16.119
        logger = PhLogging().phLogger("delete_elb_rule", LOG_DEBUG_LEVEL)
        logger.debug("elb_rule 删除流程")

        self.elb.delete_rule(self.rule_arn)
        logger.debug("elb_rule 删除完成")
