import json

from util.AWS.DynamoDB import DynamoDB
from util.ExpressionUtil import Expression
from util.NotificationType.Strategy import Strategy
from util.NotificationType.Notification import Notification


class Group(Strategy):
    def do_exec(self, data):
        # import base64
        # from util.AWS.STS import STS
        # from constants.Common import Common
        # sts = STS().assume_role(
        #     base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
        #     "Ph-Back-RW"
        # )
        # dynamodb = DynamoDB(sts=sts)
        # dynamodb = DynamoDB()
        # TODO 如何查询，是否需要历史，如何排序，是否需要对executionStatus表查询  暂时没想好
        pass
