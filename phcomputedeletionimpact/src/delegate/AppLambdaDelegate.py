import json
import handler.ExecHandler as ExecHandler


class AppLambdaDelegate:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def exec(self):
        body = json.loads(self.event.get("body"))
        type_name = body["type"]

        json_api_data = ExecHandler.makeData(type_name, body)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
            },
            "body": json.dumps(json_api_data)
        }
