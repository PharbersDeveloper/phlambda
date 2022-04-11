import json
from util.NotificationType.Trigger import Trigger


class AppLambdaDelegate:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def exec(self):
        event = self.event
        projectId = event["pathParameters"]["projectId"]
        ownerId = event["pathParameters"]["ownerId"]
        eventName = event["pathParameters"]["eventName"]
        data = dict({
            "projectId": projectId,
            "ownerId": ownerId,
            "eventName": eventName
        }, **json.loads(event["body"]))
        payload = Trigger(data).pull()
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
            },
            "body": payload
        }
