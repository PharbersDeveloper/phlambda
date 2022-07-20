import json

'''
通用

args:
    event = {
        "owner": "",
        "result": {
            "triggers": [],
            "steps": []
        }
    }
'''


def lambda_handler(event, context):
    #--mzhang
    print(event)

    result = {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": json.dumps(event["result"], ensure_ascii=False),
            "error": {}
        }
    }


    return result