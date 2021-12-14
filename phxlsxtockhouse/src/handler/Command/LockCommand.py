from handler.Command.Command import Command


class LockCommand(Command):

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self, data):
        self.receiver.lock(data["key"], data["value"], data.get("time", 60))


class UnLockCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self, data):
        self.receiver.unlock(data["key"])


class WatchLockCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self, data):
        return self.receiver.watch(data["key"])
