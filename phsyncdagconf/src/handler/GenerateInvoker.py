from handler.Command import Command
from handler.FilterCommand import FilterCommand
from handler.Receiver import Receiver
from handler.SelectCommand import SelectCommand
from handler.OperationNullCommand import OperationNullCommand
from handler.ScriptCommand import ScriptCommand


class GenerateInvoker:
    commands = {
        "filter": FilterCommand,
        "select": SelectCommand,
        "operation_null": OperationNullCommand,
        "script": ScriptCommand
    }

    def __execute(self, commands: [Command], runtime):
        if len(commands) == 0:
            return ""

        def write_prepare():
            codes = """    data_frame = kwargs.get("input_df")\n\n"""
            return_df = ""
            for code in list(commands):
                content = code.execute()
                codes += content["code"] + "\n\n"
                return_df = content["return_data"]
            codes += "    return {'out_df': " + return_df + "}\n\n"
            codes = "\n".join(list(map(lambda line: line, codes.split("\n"))))
            return codes

        def write_python():
            codes = """    data_frame = kwargs.get("df_'your out ds name'")\n\n"""
            return_df = ""
            for code in list(commands):
                content = code.execute()
                codes += content["code"] + "\n\n"
                return_df = content["return_data"]
            codes += "    return {'out_df': " + return_df + "}\n\n"
            codes = "\n".join(list(map(lambda line: line, codes.split("\n"))))
            return codes

        def write_r():
            codes = ""
            for code in list(commands):
                content = code.execute()
                codes += content["code"] + "\n\n"
            codes = "\n".join(list(map(lambda line: line, codes.split("\n"))))
            return codes

        funcs = {
            "python3": write_python,
            "pyspark": write_python,
            "r": write_r,
            "sparkr": write_r,
            "prepare": write_prepare
        }
        return funcs[runtime]()

    def execute(self, operator_parameters, runtime):
        operators = operator_parameters[::2]
        parameters = operator_parameters[1::2]
        cmd_instance = list(map(lambda item: self.commands[item[-1]](Receiver(), parameters[item[0]]),
                                enumerate(operators)))
        return self.__execute(cmd_instance, runtime)
