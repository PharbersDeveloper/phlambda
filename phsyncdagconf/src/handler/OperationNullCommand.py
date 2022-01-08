from handler.Command import Command
from util.AWS.ph_s3 import PhS3
from util.AWS import define_value as dv


class OperationNullCommand(Command):

    def __init__(self, receiver, args):
        self.receiver = receiver
        self.args = args
        self.phs3 = PhS3()

    def execute(self, data=None):
        path = "/home/hbzhao/PycharmProjects/pythonProject/phlambda/phsyncdagconf/src/phjobs/operation_null_for_pyspark.template"
        self.phs3.download(dv.TEMPLATE_BUCKET,
                           dv.CLI_VERSION + dv.TEMPLATE_OPERATOR_OPERATION_NULL_FILE_PY,
                           path)
        content = list(filter(lambda line: line != "", self.receiver.execute(path).split("\n")))
        return_data = content[-1]
        default_value = ""
        try:
            default_value = int(self.args)
        except ValueError as e:
            default_value = f"'{self.args}'"
        code = "\n".join(content[:-1]).replace("#operation_null_default#", str(None) if self.args == "" else str(default_value))
        return {
            "code": code,
            "return_data": return_data
        }
