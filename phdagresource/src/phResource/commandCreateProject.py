
from phResource.command import Command
from util.AWS.CFN import CFN
from util.AWS.ELB import ELB
from util.AWS.EC2 import EC2
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class CommandCreateProject(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.cfn = CFN()
        self.elb = ELB()
        self.ec2 = EC2()

    def execute(self):
        # 192.168.16.119
        logger = PhLogging().phLogger("creat_ec2", LOG_DEBUG_LEVEL)
        logger.debug(self.target_name)
        logger.debug(self.target_ip)
        Priority = self.elb.get_rules_len()
        # 获取当前project 的 volume id
        volumeId = self.ec2.get_volume_id(self.project_id)
        logger.debug("-----------------------")
        logger.debug(volumeId)
        logger.debug("=======================")
        self.cfn.create_project(self.target_name, self.target_ip, self.project_id, str(Priority), volumeId)
