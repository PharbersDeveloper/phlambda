import json


'''
这个函数做一件事情写入dataset dynamodb
args = {
    "traceId": "String",
    "projectId": "String",
    "owner": "String",
    "showName": "String",
    "datasets": [
        {
            "name": "String",
            "cat": "intermediate",
            "format": "parquet"
        }
    ]
}

return = {
    [
        {
            "id": "String"         # 生成的Id
            "name": "String",
            "cat": "intermediate",
            "format": "parquet"
        }
    ]   
}
'''
def lambda_handler(event, context):
    
    # 1. 只做一件事情，写dataset dynamodb，id在这里创建

    return { 
        event['datasets']
    }
