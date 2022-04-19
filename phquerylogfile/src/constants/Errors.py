
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
        "en": "File Not Found",
        "zh": "文件未找到"
    }
