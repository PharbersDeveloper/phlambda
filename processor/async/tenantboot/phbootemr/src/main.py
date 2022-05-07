import json


'''
这个从resource表中读取需要创建的资源的matedata的描述
这里通过matadata的描述启动emr
调用以前的emr启动流程

args = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "resources": [
        "emr", "ec2"
    ]，
    "metadata": {
        "emr": {
            "Common": {
                "RootVolumeSize": 10,
                "ReleaseLabel": "emr-6.2.0"
            },
            "Master": {
                "MasterInstanceType": "m5.2xlarge",
                "MasterStorage": 64
            },
            "Core": {
                "CoreInstanceType": "m5.2xlarge"
                "CoreStorage": 32,
                "InitialCoreSize": 1,
                "MaxCoreSize": 2
            },
            "Task": {
                "TaskInstanceType": "m5.2xlarge",
                "TaskStroage": 32,
                "TaskNodeOutThreshold": 10,
                "InitialTaskSize": 2,
                "MaxTaskSize": 10
            }
        }
    }
}

return = {
    
}
'''
def lambda_handler(event, context):

    return True
