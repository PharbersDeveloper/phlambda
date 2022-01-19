import subprocess

from phResource.command import Command


class CommandPutParameter(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def put_parameter(self):

        pass

    def execute(self):
        # 192.168.16.119

        self.create_dir()

        pass
