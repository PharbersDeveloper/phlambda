import json
import re
from util.ExpressionUtil import Expression
from util.Convert2JsonAPI import Convert2JsonAPI
from util.AWS.DynamoDB import DynamoDB
from models.Execution import Execution
from models.Step import Step
from models.Action import Action
from models.ProjectFile import ProjectFile
from models.Partition import Partition


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
        self.func_structure = {
            "query": self.dynamodb.queryTable,
            "scan": self.dynamodb.scanTable,
            "put_item": self.dynamodb.putData,
        }
        self.table_structure = {
            "execution": Execution,
            "step": Step,
            "action": Action,
            "project_files": ProjectFile,
            "partition": Partition
        }

    def exec(self):
        method = self.event.get("httpMethod")
        type = self.event.get("pathParameters").get("type")
        body = json.loads(self.event.get("body"))
        re_type = r"(^query$)|(^scan$)|($put_item&)"
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

        dy_method = self.func_structure[type]
        table = body["table"]
        if bool(re.match(r"(^query$)|(^scan$)", type)):
            limit = body["limit"]
            start_key = "" if len(body["start_key"]) == 0 else body["start_key"]
            conditions = body["conditions"]

            expr = Expression().join_expr(type, conditions)
            payload = dy_method({"table_name": table, "limit": limit, "expression": expr, "start_key": start_key})

            result = list(map(lambda item: self.table_structure[table](item), payload["data"]))
            json_api_data = json.loads(Convert2JsonAPI(self.table_structure[table], many=True).build().dumps(result))
            json_api_data["meta"] = {
                "start_key": payload["start_key"]
            }
        else:
            payload = dy_method({"table_name": table,"item": body["item"]})
            result = self.table_structure[table](payload["data"])
            json_api_data = json.loads(Convert2JsonAPI(self.table_structure[table], many=False).build().dumps(result))

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
#             # "type": "put_item"
#         },
#         "body": "{\"table\": \"project_files\",\"conditions\": {\"smID\": \"Auto_max_refactor\"},\"limit\": 10,\"start_key\": {}}",
#         # "body": "{\"table\": \"action\",\"item\": {\"projectId\": \"xx1ioq\", \"owner\": \"qq\", \"showName\": \"alex\", \"time\": 1635338830187, \"code\": \"1\", \"jobDesc\": \"test\", \"jobCat\": \"aaaa\", \"comments\": \"aaa\", \"message\": \"dadas\", \"date\":1635338845343}}"
#     })
#     a = app.exec()
#     print(a)
