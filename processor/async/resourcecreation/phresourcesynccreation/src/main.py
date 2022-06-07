import json
import os

'''
创建 sync
args = {
    "traceId": "String",
    "projectId": "String",
    "owner": "String",
    "showName": "String",
    "dagName": "String",
    "owner": "String",
    "projectName": "String",
    "scripts": {
        "id": "String",
        "runtime": "String",
        "name": "String",
        "flowVersion": "developer",
        "inputs": "[]",
        "output": "{}"
    },
}
'''

'''
phjob
spark.read()
df.write()

phmain
input，output
无sample，写clickhouse
version，同步到version表
'''


def lambda_handler(event, context):
    print(event)
    result = event["script"]
    
    return result
