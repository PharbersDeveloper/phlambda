import json


'''
这个函数是对所有的personal resouce boot 的 clean up
args = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "personalResBoots",
        "desc": "reboot project",
        "comments": "something need to say",
        "message": "something need to say",
        "required": true
    },
    "resourceId": "",
    "stackName:": "",
    "notification": {
        "required": true
    }
}
'''
def lambda_handler(event, context):
    
    # 1. stackName 存在就删除

    return True
