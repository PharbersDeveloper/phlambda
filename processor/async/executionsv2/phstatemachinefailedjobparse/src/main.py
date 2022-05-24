import os
import json


def lambda_handler(event, context):
    print(event)
    message = json.loads(event["error"]["Cause"])

    return message["StepId"]
