from util.NotificationType.Context import Context
from util.NotificationType.PTP import PTP
from util.NotificationType.Group import Group


class Trigger:
    functions = {
        "ptp": PTP,
        "group": Group
    }

    def __init__(self, data):
        self.data = data

    def pull(self):
        suffix = self.data["type"].lower()
        method = self.functions.get(suffix, None)
        if method is None:
            raise Exception(f"Unrealized {suffix} parsing")
        ctx = Context(method())
        return ctx.run(self.data)

