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
    
    # 1. action.cat 只能是 tenantStop
    # 2. resources 当前只能是以下值的一种
    #     2.1 emr: 暂时不支持，只是为以后project reboot => tenant reboot 做准备
    #     2.2 ec2 (deprecated 以后会被无服务器替换)
    #     2.3 clickhouse: 暂时不支持，以后用ecs 构建解决
    #     2.3 chproxy: 暂时不支持，以后用ecs 构建解决
    #     2.4 dns (deprecated 以后会被无服务器替换)
    #     2.5 target group (deprecated 以后会被无服务器替换)
    #     2.7 load balance rule (deprecated 以后会被无服务器替换)

    return True
