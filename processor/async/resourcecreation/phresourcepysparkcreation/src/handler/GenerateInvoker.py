import json
from handler.Command import Command
from handler.Receiver import Receiver
from handler.ScriptCommand import ScriptCommand


class GenerateInvoker:
    commands = {
        "script": ScriptCommand
    }

    def __execute(self, commands: [Command], runtime):
        def write_prepare():
            codes = BaseCodeCommand(Receiver()).execute()
            codes += """\ndef execute(**kwargs):\n"""
            codes += """    data_frame = kwargs.get("input_df")\n\n"""
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
        cmd_instance = list(map(lambda item: self.commands[item["type"].lower()](Receiver(), json.dumps(item)),
                                operator_parameters))

        if len(cmd_instance) == 0:
            return ""

        return self.__execute(cmd_instance, runtime)
