from string import Template
from util.AWS.ph_s3 import PhS3


class GenerateInvoker:
    def __init__(self):
        self.phs3 = PhS3()

    def __little_camel(self, item):
        return item[0].lower() + item[1:]

    def execute(self, steps, code_yaml, ds):
        def gen_code(item):
            key = self.__little_camel(item["type"])
            code = code_yaml["code"][key]["code"]
            return "\n".join(list(map(lambda x: f"    {x}", Template(code).substitute({"args": item}).split("\n"))))

        base_funcs = code_yaml["code"]["baseFuncs"]["code"]

        phjob = code_yaml["code"]["phjob"]["code"]

        codes = Template(phjob).substitute({
            "input": ds,
            "base_func": base_funcs,
            "code_fragments": "\n".join(list(map(gen_code, steps)))
        })

        return codes
