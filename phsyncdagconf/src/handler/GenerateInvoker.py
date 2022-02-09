from handler.gencode.GenCode import GenCode


class GenerateInvoker:
    # def __execute(self, strategies: [Strategy]):
    #     if len(strategies) == 0:
    #         return ""
    #     codes = """    data_frame = kwargs.get("input_df")\n\n"""
    #     return_df = ""
    #     for code in list(strategies):
    #         content = code.execute()
    #         codes += content["code"] + "\n\n"
    #         return_df = content["return_data"]
    #     codes += "    return {'out_df': " + return_df + "}\n\n"
    #     codes = "\n".join(list(map(lambda line: line, codes.split("\n"))))
    #     return codes

    def execute(self, runtime, parameters):
        gen_code_result = list(map(lambda parameter: GenCode(runtime, parameter).execute(), parameters))
        if len(gen_code_result) == 0:
            return ""
        codes = ""
        if runtime.lower() == "pyspark":
            codes += """    data_frame = kwargs.get("input_df")\n\n"""

        return_df = ""
        for content in gen_code_result:
            codes += content["code"] + "\n"
            return_df = content["return_data"]
        codes += "    return {'out_df': " + return_df + "}\n"
        codes = "\n".join(list(map(lambda line: line, codes.split("\n"))))

        return codes
