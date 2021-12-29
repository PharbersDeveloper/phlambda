from handler.Context import Context
from handler.Xlsx import Xlsx
from constants.Errors import NoImplError


class Reader:
    functions = {
        "xlsx": Xlsx,
    }

    def __init__(self, data):
        self.data = data

    def reader(self):
        temp_file = self.data.get("tempfile", "")
        suffix = temp_file.split(".")[-1].lower()
        method = self.functions.get(suffix, None)
        if method is None:
            raise NoImplError(f"Unrealized {suffix} parsing")
        ctx = Context(method())
        return ctx.run(self.data)
