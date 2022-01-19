
from phResource.command import Command
from util.AWS.ELB import ELB


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

        self.elb.register_targets(self.target_group_arn, targets)
        pass