import json


'''
这个函数清理已经操作的东西，保证操作的原子性
args = {
    "traceId": "String",
    "projectId": "String",
    "owner": "String",
    "showName": "String",
    "traceId": "String",
    "projectId": "String",
    "owner": "String",
    "showName": "String",
    "datasets": [
        {
            "id": "String",
            "name": "String",
            "cat": "intermediate",
            "format": "parquet"
        }
    ],
    "scripts": {
        "id": "String",
        "jobName": "String",
        "actionName": "String",
        "flowVersion": "developer",
        "inputs": "[]",
        "output": "{}"
    },
    "errors": {
        "Error": "Exception",
        "Cause": ""
    }
}
'''
def lambda_handler(event, context):
    
    # 1. 如果dataset name在dataset中存在，删除
    # 2. 如果scripts name在dataset中存在，删除
    # 3. 如果dag表中，ctype = node && represent-id 为上诉中的已经被删除的节点删除
    # 4. 如果dag表中，ctype = node && cmessage 中 sourceId 或者 targetId 为上述中的删除节点的删除
    # 5. 删除s3中目标文件夹的文件
    #   5.1 每一个生成过程都给一个TraceID命名的文件，如果文件名一样，删除，如果文件不一样说明时别人创建的不能删除

    return True
