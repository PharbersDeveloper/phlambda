import os
import json


def lambda_handler(event, context):
    # cicd 0717 1206
    print(event)
    message = json.loads(event["error"]["Cause"])

    return message["StepId"]
