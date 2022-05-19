import json


'''
这个函数是对所有的reboot的数据参数的validate
args = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "personalResStops",
        "desc": "reboot project",
        "comments": "something need to say",
        "message": "something need to say",
        "required": true
    },
    "resourceId": "",
    "notification": {
        "required": true
    }
}
'''
def lambda_handler(event, context):
    
    # 1. action.cat 只能是 personalResStops
    # 2. resourcesId 必须存在
    # 3. ssm 中必须存在 key 为 tenantId的项

    return True
