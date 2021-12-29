
class Errors(Exception):
    code = -1
    message = {
        "en": "unknown error",
        "zh": "未知错误"
    }

    def __init__(self, msg):
        self.message["meta"] = str(msg)


class FileNotFound(Errors):
    code = 404
    message = {
        "en": "File Not Found",
        "zh": "文件未找到"
    }


class NotXlsxFile(Errors):
    code = 500
    message = {
        "en": "The File Is Not Xlsx Type",
        "zh": "该文件不是xlsx `Excel 2007+ 版本` 的文件"
    }


class NotXlsFile(Errors):
    code = 501
    message = {
        "en": "The File Is Not Xls Type",
        "zh": "该文件不是xls `Excel 2007 版本` 的文件"
    }


class NotCsvFile(Errors):
    code = 503
    message = {
        "en": "Comma Separated Failure",
        "zh": "默认以逗号 `,` 分割失败"
    }


class NotParquetFile(Errors):
    code = 504
    message = {
        "en": "The File Is Not Parquet Type",
        "zh": "该文件不是 `Parquet` 类型"
    }


class NoImplError(Errors):
    code = 10
    message = {
        "en": "Function Not Implement",
        "zh": "处理方式未开发"
    }
