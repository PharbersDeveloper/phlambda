import json


class Errors(Exception):
    code = -1
    message = {
        "en": "unknown error",
        "zh": "未知错误"
    }

    def __init__(self, msg):
        self.message["meta"] = str(msg)


class NoImplError(Errors):
    code = 10
    message = {
        "en": "Function Not Implement",
        "zh": "处理方式未开发"
    }


class FileNotFound(Errors):
    code = 404
    message = {
        "en": "create dag_conf failed",
        "zh": "创建dag_conf错误"
    }


class DagConfFailed(Errors):
    code = 500
    message = {
        "en": "create dag_conf failed",
        "zh": "创建dag_conf失败"
    }


class DagLevelFailed(Errors):
    code = 501
    message = {
        "en": "create dag_level failed",
        "zh": "创建dag_level失败"
    }


class DagItemFailed(Errors):
    code = 503
    message = {
        "en": "create dag_item failed",
        "zh": "创建dag_item时错误"
    }


class NotParquetFile(Errors):
    code = 504
    message = {
        "en": "The File Is Not Parquet Type",
        "zh": "上传dag_item时错误"
    }


class SchemaNotMatched(Errors):
    code = 505
    message = {
        "en": "Schema Not Matched",
        "zh": "Schema与原有不匹配，请使用高级映射"
    }


class VersionAlreadyExist(Errors):
    code = 506
    message = {
        "en": "Version Already Exist",
        "zh": "版本已经存在"
    }


class ResourceBusy(Errors):
    code = 507
    message = {
        "en": "Resources Are Busy",
        "zh": "资源正在被使用"
    }


def serialization(data):
    content = {
        "code": 200,
        "message": data
    }
    if isinstance(data, Exception):
        content["code"] = data.code
        content["message"] = data.message
    return json.dumps(content, ensure_ascii=False)
