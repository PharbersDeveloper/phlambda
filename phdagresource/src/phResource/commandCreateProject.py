
from phResource.command import Command
from util.AWS.CFN import CFN
from util.AWS.ELB import ELB
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class CommandCreateProject(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.cfn = CFN()
        self.elb = ELB()

    def execute(self):
        # 192.168.16.119
        logger = PhLogging().phLogger("creat_ec2", LOG_DEBUG_LEVEL)
        logger.debug(self.target_name)
        logger.debug(self.target_ip)
        Priority = self.elb.get_rules_len()
        logger.debug("========================")
        logger.debug(Priority)
        logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>")
        self.cfn.create_project(self.target_name, self.target_ip, self.project_id, str(Priority))
