
class Errors(Exception):
    code = -1
    message = {
        "en": "unknown error",
        "zh": "未知错误"
    }

    def __init__(self, msg):
        self.message["meta"] = str(msg)


class FileNotFound(Errors):
    code = 0
    message = {
        "en": "File Not Found",
        "zh": "文件未找到"
    }


class DynamoDBNotItem(Errors):
    code = 1
    message = {
        "en": "DynamoDB Not Item",
        "zh": "DynamoDB 未找到数据"
    }


class FileCodeError(Errors):
    code = 2
    message = {
        "en": "File Code Error",
        "zh": "文件编码异常"
    }


class ItemLogsError(Errors):
    code = 3
    message = {
        "en": "dyanmoDB item logs error",
        "zh": "item日志信息错误"
    }


class ItemTypeError(Errors):
    code = 4
    message = {
        "en": "dyanmoDB item logs type error",
        "zh": "item日志type错误"
    }
