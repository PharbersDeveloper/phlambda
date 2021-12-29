from handler.Strategy.Context import Context
from handler.Strategy.Xlsx import Xlsx
from constants.Errors import NoImplError


class Reader:
    functions = {
        "xlsx": Xlsx,
    }

    def __init__(self, data):
        self.data = data

    def reader(self):
        suffix = self.data["message"]["fileType"].lower()
        method = self.functions.get(suffix, None)
        if method is None:
            raise NoImplError(f"Unrealized {suffix} parsing")
        ctx = Context(method())
        return ctx.run(self.data)
