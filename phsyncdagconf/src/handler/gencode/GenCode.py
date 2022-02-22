from handler.gencode.Context import Context
from handler.gencode.strategy.FilterOnValueStrategy import FilterOnValueStrategy
from handler.gencode.strategy.FilterOnNumericalRangeStrategy import FilterOnNumericalRangeStrategy
from handler.gencode.strategy.RemoveRowsOnEmptyStrategy import RemoveRowsOnEmptyStrategy
from handler.gencode.strategy.SelectStrategy import SelectStrategy
from handler.gencode.strategy.ScriptStrategy import ScriptStrategy


class GenCode:
    commands = {
        "Script": ScriptStrategy,
        "FilterOnValue": FilterOnValueStrategy,
        "FilterOnNumericalRange": FilterOnNumericalRangeStrategy,
        "RemoveRowsOnEmpty": RemoveRowsOnEmptyStrategy,
        "Select": SelectStrategy,
    }

    def __init__(self, runtime, parameter):
        self.parameter = parameter
        self.runtime = runtime

    def execute(self):
        type_name = self.parameter["type"]
        function = self.commands.get(type_name, None)
        if function is None:
            raise "No Impl Error"

        ctx = Context(function())
        return ctx.do_execution({
            "runtime": self.runtime,
            "parameter": self.parameter
        })

