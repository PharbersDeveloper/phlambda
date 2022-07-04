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

def delete_resource(event):
    return {
        "desc": event["jobDesc"] 
    }


def create_ds(event):
    datasets = event["result"]["datasets"]
    names = list(map(lambda item: item["name"], datasets))
    return { "datasets": names }


def create_script(event):
    script = event["result"]["script"]
    job_name = "_".join([script["flowVersion"], script["id"], 
    event["projectName"], event["dagName"], script["name"]])

    return {
        "jobName": job_name,
        "jobShowName": script["name"],
        "jobId": script["id"],
        "runtime": script["runtime"]
    }

def return_cat(event):
    if "jobCat" in event and event["jobCat"] == "deleteResource":
        return "delete_resource"
    
    script = event["result"]["script"]
    if script["runtime"] == "dataset" and "name" not in script:
        return "create_ds"
    
    return "create_script"

def lambda_handler(event, context):
    print(event)

    result = {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": {}
        }
    }

    cat_funcs = {
        "delete_resource": delete_resource,
        "create_ds": create_ds,
        "create_script": create_script
    }
    cat = return_cat(event)
    content = cat_funcs[cat](event)
    result["cnotification"]["data"] = content

    return result