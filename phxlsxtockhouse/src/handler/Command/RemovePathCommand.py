import os
from handler.Command.Command import Command


class RemovePathCommand(Command):

    def execute(self, path):
        os.system("rm -rf " + path)
