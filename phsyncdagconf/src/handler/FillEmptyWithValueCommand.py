import json
from handler.Command import Command
from util.AWS.ph_s3 import PhS3
from util.AWS import define_value as dv


class FillEmptyWithValueCommand(Command):

    def __init__(self, receiver, args):
        self.receiver = receiver
        self.args = args
        self.phs3 = PhS3()

    def execute(self, data=None):
        data = json.loads(self.args)
        runtime = data["code"]
        file = f"fill_empty_with_value_for_{runtime}"
        path = f"/tmp/phjobs/${file}.template"
        # path = f"/Users/qianpeng/GitHub/phlambda/phsyncdagconf/src/phjobs/{file}.template"
        self.phs3.download(dv.TEMPLATE_BUCKET,
                           dv.CLI_VERSION + dv.LOW_CODE_TEMPLATE_OPERATOR[file],
                           path)
        content = list(filter(lambda line: line != "", self.receiver.execute(path).split("\n")))
        return_data = content[-1]
        code = "\n".join(content[:-1]).replace("#fill_empty_parameter#", str(data))
        return {
            "code": code,
            "return_data": return_data
        }
