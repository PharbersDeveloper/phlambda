import json


'''
这个函数做一件事情，写dagconf dynamodb
args = {
    "traceId": "String",
    "projectId": "String",
    "owner": "String",
    "showName": "String",
    "script": {
        "actionName": "compute_C2",
        "flowVersion": "developer",
        "inputs": "[]",
        "output": "{}"
    }
}

return =  
    {
        "id": "String",                 # 生成的ID
        "jobName": "String",
        "actionName": "String",
        "flowVersion": "developer",
        "inputs": "[]",
        "output": "{}"
    }
'''
def lambda_handler(event, context):
    
    # 1. 只做一件事情，写dagconf dynamodb，id在这里创建

    return { 
        event['script']
    }
