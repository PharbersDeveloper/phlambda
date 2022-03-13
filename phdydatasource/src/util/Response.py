import json


class Response:
    headers = {
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
    }

    statusCode = 200

    body = ""

    def __init__(self, body, code):
        self.body = body
        self.statusCode = code

    @property
    def build(self):
        return {
            "statusCode": self.statusCode,
            "headers": self.headers,
            "body": json.dumps(self.body)
        }
