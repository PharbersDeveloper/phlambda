from handler.Command.Command import Command


class CheckSchemaConsistencyCommand(Command):

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self, data):
        if data["ds_schema"] is not None:
            self.receiver.check(data)


