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
s3path: 
s3://ph-platform/2020-11-11/jobs/python/phcli/<projectName>_<projectName>_<scripts.flowVersion>/<projectName>_<projectName>_<scripts.flowVersion>_<script.name>

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
