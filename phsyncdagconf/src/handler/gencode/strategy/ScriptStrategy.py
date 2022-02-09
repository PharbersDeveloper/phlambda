from handler.gencode.Strategy import Strategy
from util.AWS import define_value as dv


class ScriptStrategy(Strategy):

    def do_execution(self, data):
        runtime = data["runtime"]
        parameter = data["parameter"]
        path = "/tmp/phjobs/script.template"
        self.phs3.download(dv.TEMPLATE_BUCKET,
                           dv.CLI_VERSION + dv.TEMPLATE_OPERATOR[runtime],
                           path)

        content = list(filter(lambda line: line != "", self.load(path).split("\n")))
        return_data = content[-1]
        # code = "\n".join(content[:-1]).replace("#filter_kvs#", str(self.args))
        code = ""
        return {
            "code": code,
            "return_data": return_data
        }
