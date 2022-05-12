import json

'''
通用

args:
    event = {
        "owner": "",
        "result": {
            "datasets": [
                {
                    "name": "Alex",
                    "cat": "uploaded",
                    "format": "parquet",
                    "id": "f1801eb22d79cbd6325d23ca74fc954e.xlsx"
                },
                {
                    "name": "333a",
                    "cat": "intermediate",
                    "format": "parquet",
                    "id": "5M9K2145jA7WEab"
                }
            ],
            "script": {
                "name": "compute_333a",
                "flowVersion": "developer",
                "runtime": "r",
                "inputs": "[\"Alex\"]",
                "output": "333a",
                "id": "1kunO6Fyc0Rg3jz"
            }
        }
    }
'''

def lambda_handler(event, context):
    print(event)
    datasets = event["result"]["datasets"]
    script = event["result"]["script"]
    result = {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": {}
        }
    }

    if script["runtime"] == "dataset" and "name" not in script:
        names = list(map(lambda item: item["name"], datasets))
        result["cnotification"]["data"] = {
            "datasets": names
        }
    else:
        result["cnotification"]["data"] = {
            "jobName": f"""{script["flowVersion"]}_{script["id"]}_{event["projectName"]}_{event["dagName"]}_{script["name"]}""",
            "jobShowName": script["name"],
            "runtime": script["runtime"]
        }

    return result