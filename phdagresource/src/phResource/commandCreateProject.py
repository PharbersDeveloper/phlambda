
from phResource.command import Command
from util.AWS.CFN import CFN


class CommandCreateProject(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.cfn = CFN()

    def execute(self):
        # 192.168.16.119

        self.cfn.create_project(self.target_name)
