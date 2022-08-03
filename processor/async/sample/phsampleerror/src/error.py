import json


class Errors(Exception):
    errorcode = -1
    errormessage = {
        "en": "unknown error",
        "zh": "未知错误"
    }

    def __init__(self, msg):
        self.message["meta"] = str(msg)


class NoImplError(Errors):
    errorcode = -99
    errormessage = {
        "en": "Function Not Implement",
        "zh": "处理方式未开发"
    }


class FileNotFound(Errors):
    errorcode = -101
    errormessage = {
        "en": "File Not Found",
        "zh": "文件未找到"
    }


class NotXlsxFile(Errors):
    errorcode = -102
    errormessage = {
        "en": "The File Is Not Xlsx Type",
        "zh": "该文件不是xlsx `Excel 2007+ 版本` 的文件"
    }


class NotXlsFile(Errors):
    errorcode = -103
    errormessage = {
        "en": "The File Is Not Xls Type",
        "zh": "该文件不是xls `Excel 2007 版本` 的文件"
    }


class NotCsvFile(Errors):
    errorcode = -104
    errormessage = {
        "en": "Comma Separated Failure",
        "zh": "默认以逗号 `,` 分割失败"
    }


class NotParquetFile(Errors):
    errorcode = -105
    errormessage = {
        "en": "The File Is Not Parquet Type",
        "zh": "该文件不是 `Parquet` 类型"
    }


class SchemaNotMatched(Errors):
    errorcode = -201
    errormessage = {
        "en": "Schema Not Matched",
        "zh": "Schema与原有不匹配，请使用高级映射"
    }


class VersionAlreadyExist(Errors):
    errorcode = -202
    errormessage = {
        "en": "Version Already Exist",
        "zh": "版本已经存在"
    }


class ResourceBusy(Errors):
    errorcode = -801
    errormessage = {
        "en": "Resources Are Busy",
        "zh": "资源正在被使用"
    }


class ColumnDuplicate(Errors):
    errorcode = -203
    errormessage = {
        "en": "Duplicate Column Names",
        "zh": "重复的列名"
    }


def serialization(data):
    content = {
        "code": 200,
        "data": data
    }
    if isinstance(data, Exception):
        content["error"] = {}
        content["error"]["errorcode"] = data.errorcode
        content["error"]["errormessage"] = data.errormessage

    return json.dumps(content, ensure_ascii=False)
