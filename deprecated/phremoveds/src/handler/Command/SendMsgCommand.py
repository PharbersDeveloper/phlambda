from handler.Command.Command import Command


class SendMsgSuccessCommand(Command):

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self, data):
        self.receiver.succeed(data)


class SendMsgFailCommand(Command):

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self, data):
        self.receiver.failed(data)

