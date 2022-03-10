
from handler.Command.Command import Command


class WriteS3Command(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self, data):
        self.receiver.write(data)
