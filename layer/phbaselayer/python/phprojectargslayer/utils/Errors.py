import json


class Errors(Exception):
    code = -1
    message = {
        "en": "unknown error",
        "zh": "未知错误"
    }

    def __init__(self, msg):
        self.message["meta"] = str(msg)


class ResourceNotCreateError(Errors):
    code = 10
    message = {
        "en": "Resource Not Create",
        "zh": "资源未创建"
    }


class FileNotFound(Errors):
    code = 404
    message = {
        "en": "File Not Found",
        "zh": "文件未找到"
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
