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
        category = data.get("category", "").lower()
        method = self.strategy_fun.get(category, None)
        if method is not None:
            ctx = Context(method())
            ctx.run(data)


if __name__ == "__main__":
    ChoiceMain().choice({
        "category": "Xlsx",
        "sql": "SELECT `通用名称`, `商品名称`, `生产企业`, `剂型`, `规格`, `包装数量`, `包装单位`, `PACKCODE`, `项目`, `version` FROM default.`测试analyze` WHERE 1 = 1 LIMIT 200 OFFSET 0",
        "schema": ["通用名称", "商品名称", "生产企业", "剂型", "规格", "包装数量", "包装单位", "PACKCODE", "项目", "version"]
    })
