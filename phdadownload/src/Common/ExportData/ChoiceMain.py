import json
from Context import Context
from XlsxStrategy import XlsxStrategy
from CsvStrategy import CsvStrategy
from ParquetStrategy import ParquetStrategy


class ChoiceMain:

    strategy_fun = {
        "csv": CsvStrategy,
        "xlsx": XlsxStrategy,
        "parquet": ParquetStrategy,
        "xls": None,
    }

    def __init__(self):
        pass

    def choice(self, data) -> None:
        body = json.loads(data.get('body'))
        category = body.get("category", "").lower()
        method = self.strategy_fun.get(category, None)
        if method is not None:
            ctx = Context(method())
            return ctx.run(body)


if __name__ == "__main__":
    ChoiceMain().choice({"category": "parquet",
                         "sql": "SELECT `id`, `name`, `gender`, `test` FROM default.`student`",
                         "schema": ["id", "name", "gender", "test"],
                         "file_name": "test23.parquet"})
