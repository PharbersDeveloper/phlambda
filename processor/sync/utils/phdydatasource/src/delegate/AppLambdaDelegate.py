import json
import re
import handler.ExecHandler as ExecHandler
from models.PhError import PhError
from util.Response import Response


class AppLambdaDelegate:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def exec(self):
        try:
            method = self.event.get("httpMethod").lower()
            type = self.event.get("pathParameters").get("type")
            body = json.loads(self.event.get("body"))
            re_type = r"(^query$)|(^scan$)|(^put_item$)|(^delete_item$)"
            re_method = r"^post$"
            if (not bool(re.match(re_method, method))) | (not bool(re.match(re_type, type))):
                return Response(PhError("invalid parameter", f"{method}:{type}").messages, 403).build

            table = body["table"]

            json_api_data = ExecHandler.makeData(table, body, type)

            return Response(json_api_data, 200).build
        except Exception as e:
            print("*"*50 + "ERROR" + "*"*50, str(e))
            return Response(PhError(str(e)).messages, 500).build
