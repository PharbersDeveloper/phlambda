import json


'''
开工没有回头箭，这里只能强行清理
这里暂时不做任何事情
args = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "tenantStop",
        "desc": "reboot project",
        "comments": "something need to say",
        "message": "something need to say",
        "required": true
    },
    "resources": [
        "emr", "chlickhouse", "chproxy"
    ],
    "notification": {
        "required": true
    }
}
'''
def lambda_handler(event, context):
    # 理论上 stack的回滚会在 cf 里面执行
    # 所以 clean up 不需要做啥事情
    return True
