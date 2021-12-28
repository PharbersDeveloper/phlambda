from handler.Command import Command
from handler.FilterCommand import FilterCommand
from handler.Receiver import Receiver
from handler.SelectCommand import SelectCommand
from handler.OperationNullCommand import OperationNullCommand


class GenerateInvoker:
    commands = {
        "filter": FilterCommand,
        "select": SelectCommand,
        "operation_null": OperationNullCommand
    }

    def __execute(self, commands: [Command]):
        if len(commands) == 0:
            return ""
        codes = """
    data_frame = kwargs.get("input_df")\n\n"""
        return_df = ""
        for code in list(commands):
            content = code.execute()
            codes += content["code"] + "\n\n"
            return_df = content["return_data"]
        codes += "    return {'out_df': " + return_df + "}\n\n"
        codes = "\n".join(list(map(lambda line: "    " + line, codes.split("\n"))))
        return codes

    def execute(self, args):
        operators = args[::2]
        parameters = args[1::2]
        cmd_instance = list(map(lambda item: self.commands[item[-1]](Receiver(), parameters[item[0]]),
                                enumerate(operators)))
        return self.__execute(cmd_instance)
