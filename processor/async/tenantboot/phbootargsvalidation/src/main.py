import json
import boto3
from boto3.dynamodb.conditions import Key


'''
这个函数是对所有的reboot的数据参数的validate
args = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "tanentId": "pharbers",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "tenantStart",
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


ssm = boto3.client('ssm')
cloudformation = boto3.client('cloudformation')
dynamodb = boto3.resource("dynamodb")


class Check:

    def check_ssm(self, tenantId):
        try:
            response = ssm.get_parameter(
                Name=tenantId
            )
            raise Exception(f"stack_Name in ssm already exits tenantId: {tenantId}")
        except:
            pass

    def check_parameter(self, data):

        # 1. action.cat 只能是 tenantStart
        if not data.get("action").get("cat") == "tenantStart":
            raise Exception('action.cat not tenantStart')

        # 2. resources 当前只能是以下值的一种
        resources_args = ["emr", "ec2", "clickhouse", "chproxy", "dns", "target group", "load balance rule"]

        resources = data.get("resources")
        for resource in resources:
            if resource not in resources_args:
                raise Exception('resouces error')

        tenantId = data["common"]["tenantId"]
        self.check_ssm(tenantId)
        return True


def lambda_handler(event, context):
    print(event)
    return Check().check_parameter(event)
    # 1. action.cat 只能是 tenantStart
    # 2. resources 当前只能是以下值的一种
    #     2.1 emr: 暂时不支持，只是为以后project reboot => tenant reboot 做准备
    #     2.2 ec2 (deprecated 以后会被无服务器替换)
    #     2.3 clickhouse: 暂时不支持，以后用ecs 构建解决
    #     2.3 chproxy: 暂时不支持，以后用ecs 构建解决
    #     2.4 dns (deprecated 以后会被无服务器替换)
    #     2.5 target group (deprecated 以后会被无服务器替换)
    #     2.7 load balance rule (deprecated 以后会被无服务器替换)
    # 3. 当resource不存在的时候，启动全部记录在数据库中的参数
