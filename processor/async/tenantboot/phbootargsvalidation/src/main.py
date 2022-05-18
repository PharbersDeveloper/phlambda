import json
import boto3

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

class Check:

    def get_cloudformation_stack(self):
        cloudformation = boto3.client('cloudformation', region_name="cn-northwest-1")
        responses = cloudformation.list_stacks().get("StackSummaries", [])
        return [response.get("StackName") for response in responses]


    def get_ssm(self):
        ssm = boto3.client('ssm', region_name="cn-northwest-1")
        responses = ssm.describe_parameters().get("Parameters")
        return [response.get("name") for response in responses]


    def check_parameter(self, data):

        # 1. action.cat 只能是 tenantStart
        if not data.get("action").get("cat") == "tenantStart":
            raise Exception('action.cat not tenantStart')

        # 2. resources 当前只能是以下值的一种
        stack_name = data.get("traceId")
        resources_args = ["emr", "ec2", "clickhouse", "chproxy", "dns", "target group", "load balance rule"]
        resources = data.get("resources")
        for resource in resources:
            if resource not in resources_args:
                raise Exception('resouces error')

        if stack_name in self.get_cloudformation_stack:
            raise Exception('cloudformation already exist')
        if stack_name in self.get_ssm():
            raise Exception('ssm already exist')
        return True


def lambda_handler(event, context):
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

