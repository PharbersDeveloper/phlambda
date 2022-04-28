
from handler.Command.Command import Command


class SaveCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self, data):
        self.receiver.exec(data)
