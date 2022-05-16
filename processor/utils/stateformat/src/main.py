import os
import json

'''
args:
    event = {
        "template": "",
        "args:" [
            ""
        ]
    }

return:
    format = 
    {
        
    }
'''


def lambda_handler(event, context):
    print(event)
    args = event["args"]
    return event["template"].format(*args)