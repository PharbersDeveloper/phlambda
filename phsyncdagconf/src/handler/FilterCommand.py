from handler.Command import Command
from util.AWS.ph_s3 import PhS3
from util.AWS import define_value as dv


class FilterCommand(Command):

    def __init__(self, receiver, args):
        self.receiver = receiver
        self.args = args
        self.phs3 = PhS3()

    def execute(self, data=None):
        path = "/tmp/phjobs/filter_for_pyspark.template"
        self.phs3.download(dv.TEMPLATE_BUCKET,
                           dv.CLI_VERSION + dv.TEMPLATE_OPERATOR_FILTER_FILE_PY,
                           path)

        content = list(filter(lambda line: line != "", self.receiver.execute(path).split("\n")))
        return_data = content[-1]
        code = "\n".join(content[:-1]).replace("#filter_kvs#", str(self.args))
        return {
            "code": code,
            "return_data": return_data
        }
