import json
import re
from util.ExpressionUtil import Expression
from util.Convert2JsonAPI import Convert2JsonAPI
from util.AWS.DynamoDB import DynamoDB
from models.Execution import Execution
from models.Step import Step
from models.Action import Action


class AppLambdaDelegate:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        # import base64
        # from util.AWS.STS import STS
        # from constants.Common import Common
        # sts = STS().assume_role(
        #     base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
        #     "Ph-Back-RW"
        # )
        # self.dynamodb = DynamoDB(sts=sts)
        self.dynamodb = DynamoDB()
        self.structure = {
            "query": self.dynamodb.queryTable,
            "scan": self.dynamodb.scanTable,
            "execution": Execution,
            "step": Step,
            "action": Action
        }

    def _convert_2_model(self, table, item):
        return self.structure[table](item)

    def exec(self):
        method = self.event.get("httpMethod")
        type = self.event.get("pathParameters").get("type")
        body = json.loads(self.event.get("body"))
        re_type = r"(^query$)|(^scan$)"
        re_method = r"^post$"
        if bool(re.match(re_method, method)) & \
           bool(re.match(re_type, type)):
            return {
                "statusCode": 403,
                "headers": {
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
                },
                "body": json.dumps({
                    "message": "invalid parameter"
                })
            }

        dy_method = self.structure[type]
        table = body["table"]
        limit = body["limit"]
        start_key = "" if len(body["start_key"]) == 0 else body["start_key"]
        conditions = body["conditions"]

        expr = Expression().join_expr(type, conditions)
        payload = dy_method(table, limit, expr, start_key)

        result = list(map(lambda item: self._convert_2_model(table, item), payload["data"]))
        json_api_data = json.loads(Convert2JsonAPI(self.structure[table]).mc(many=True).dumps(result))
        json_api_data["meta"] = {
            "start_key": payload["start_key"]
        }

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
            },
            "body": json.dumps(json_api_data)
        }


# if __name__ == '__main__':
#     app = AppLambdaDelegate(event={
#         "httpMethod": "POST",
#         "pathParameters": {
#             "type": "scan"
#         },
#         "body": "{\"table\": \"execution\",\"conditions\": {\"smId\": \"0iveStO4gzwMuyZx\"},\"limit\": 10,\"start_key\": {}}",
#     })
#     a = app.exec()
#     print(a)
