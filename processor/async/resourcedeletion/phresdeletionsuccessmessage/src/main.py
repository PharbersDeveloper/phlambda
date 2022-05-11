import json

'''
通用

args:
    event = {
        "runtime"
        "owner"
        "flowVersion"
        "jobId"
        "projectName"
        "dagName"
        "jobShowName"
    }
'''

def lambda_handler(event, context):
    return {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": {}
        }
    }