
from phResource.command import Command
from util.AWS.ELB import ELB
from util.AWS.SSM import SSM
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class CommandDelRule(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.elb = ELB()
        self.ssm = SSM()

    def execute(self):
        # 192.168.16.119
        logger = PhLogging().phLogger("delete_elb_rule", LOG_DEBUG_LEVEL)
        logger.debug("elb_rule 删除流程")
        # 从dynamodb 获取ruleArn
        rule_arn = self.resource_args.get("ruleArn")
        logger.debug("rule_arn")
        logger.debug(rule_arn)
        self.elb.delete_rule(rule_arn)
        logger.debug("elb_rule 删除完成")
