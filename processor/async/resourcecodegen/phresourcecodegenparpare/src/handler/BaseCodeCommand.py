from handler.Command import Command
from util.AWS.ph_s3 import PhS3
from util.AWS import define_value as dv


class BaseCodeCommand(Command):

    def __init__(self, receiver):
        self.receiver = receiver
        self.phs3 = PhS3()

    def execute(self, data=None):
        file = "base_funcs"
        path = f"/tmp/phjobs/${file}.template"
        # path = f"/Users/qianpeng/Desktop/TestCreateFIle/{file}.template"
        self.phs3.download(dv.TEMPLATE_BUCKET,
                           dv.CLI_VERSION + dv.LOW_CODE_TEMPLATE_OPERATOR[file],
                           path)
        content = list(filter(lambda line: line != "", self.receiver.execute(path).split("\n")))
        return "\n".join(content)
