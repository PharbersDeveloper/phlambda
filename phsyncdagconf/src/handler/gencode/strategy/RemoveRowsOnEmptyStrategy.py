from handler.gencode.Strategy import Strategy
from util.AWS import define_value as dv


class RemoveRowsOnEmptyStrategy(Strategy):

    def do_execution(self, data):
        runtime = data["runtime"]
        parameter = data["parameter"]

        file = f"remove_row_on_empty_for_{runtime}"
        path = f"/tmp/phjobs/{file}.template"
        self.phs3.download(dv.TEMPLATE_BUCKET,
                           dv.CLI_VERSION + dv.TEMPLATE_OPERATOR[file],
                           path)

        content = list(filter(lambda line: line != "", self.load(path).split("\n")))
        return_data = content[-1]
        default_value = ""
        try:
            print(1)
            # default_value = int(self.args)
        except ValueError as e:
            print(2)
            # default_value = f"'{self.args}'"
        # code = "\n".join(content[:-1]).replace("#operation_null_default#", str(None) if self.args == "" else str(default_value))
        code = ""
        return {
            "code": code,
            "return_data": return_data
        }
