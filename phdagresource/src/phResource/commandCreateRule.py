
from phResource.command import Command
from util.AWS.ELB import ELB


class CommandCreateRule(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.elb = ELB()

    def execute(self):
        # 192.168.16.119

        self.elb.create_rule(self.target_name, self.target_group_arn)
        pass