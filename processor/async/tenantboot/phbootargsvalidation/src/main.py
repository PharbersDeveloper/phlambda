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


ssm = boto3.client('ssm', region_name="cn-northwest-1")
cloudformation = boto3.client('cloudformation', region_name="cn-northwest-1",
                              aws_access_key_id="AKIAWPBDTVEANKEW2XNC",
                              aws_secret_access_key="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")
dynamodb = boto3.resource("dynamodb", region_name="cn-northwest-1",
                           aws_access_key_id="AKIAWPBDTVEANKEW2XNC",
                           aws_secret_access_key="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")


class Check:

    def check_ssm(self, stack_name, tenantId):
        try:
            response = ssm.get_parameter(
                Name=stack_name
            )
            raise Exception(f"stack_Name in ssm already exits tenantId: {tenantId} role: {stack_name.split('-')[0]} type: {stack_name.split('-')[1]}")
        except:
            pass

    def query_resource(self, tenantId):
        table = dynamodb.Table("resource")
        response = table.query(
            KeyConditionExpression=Key('tenantId').eq(tenantId),
        )
        return response.get("Items")

    def get_stack_name(self, tenantId):
        tenantId = "zudIcG_17yj8CEUoCTHg"
        resource_item = self.query_resource(tenantId)
        item_list = [item for item in resource_item if item.get("ownership") == "shared"]

        res_list = []
        for i in item_list:
            res_list += [f'{i.get("role")}-{j.get("type")}-{tenantId.replace("_", "-")}' for j in
                         json.loads(i.get("properties"))]
        return res_list

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
        stack_list = self.get_stack_name(tenantId)
        for stack_name in stack_list:
            self.check_ssm(stack_name, tenantId)
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
