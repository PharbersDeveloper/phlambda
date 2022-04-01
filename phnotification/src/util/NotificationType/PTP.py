import json

from util.AWS.DynamoDB import DynamoDB
from util.ExpressionUtil import Expression
from util.NotificationType.Strategy import Strategy
from util.NotificationType.Notification import Notification


class PTP(Strategy):
    def do_exec(self, data):
        # import base64
        # from util.AWS.STS import STS
        # from constants.Common import Common
        # sts = STS().assume_role(
        #     base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
        #     "Ph-Back-RW"
        # )
        # dynamodb = DynamoDB(sts=sts)
        dynamodb = DynamoDB()

        table_name = data["target"]
        if data["target"] == "notification":
            conditions = {"id": ["=", data["id"]], "projectId": ["begins_with", data["projectId"]]}
        else:
            date = data["runnerId"].split("_")[-1]
            conditions = {"id": ["=", f"""{data["id"]}"""], "date": ["=", date]}

        expr = Expression().join_expr(conditions)
        payload = dynamodb.queryTable({
            "table_name": table_name,
            "limit": 100,
            "expression": expr,
            "start_key": None
        })["data"]
        if len(payload) > 0:
            return json.dumps(Notification().transform_ptp(data["target"], payload,
                                                           data["projectId"], data["ownerId"], data["eventName"]))
        return json.dumps({})
