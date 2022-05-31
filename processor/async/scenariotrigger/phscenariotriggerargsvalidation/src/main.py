import json
import boto3

'''
这个函数是对所有的reboot的数据参数的validate
args = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "scenarioId": "alfred-resource-creation-scenarioId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "scenarioTrigger",
        "desc": "scenario trigger",
        "comments": "something need to say",
        "message": "something need to say",
        "required": true
    },
    "resourcesId": "String",
    "notification": {
        "required": true
    }
}
'''


def get_ssm():
    ssm = boto3.client('ssm', region_name="cn-northwest-1")
    responses = ssm.describe_parameters().get("Parameters")
    return [response.get("name") for response in responses]


def check_parameter(data, **kwargs):
    common = data.get("action", {})
    # 1. action.cat 只能是 personalResBoots
    if not common.get("cat") == "personalResBoots":
        raise Exception('action.cat must be personalResBoots')

    # 2. resourcesId 必须存在
    if not data.get("resourcesId"):
        raise Exception('resourcesId not exits')

    # 3. ssm 中必须存在 key 为 tenantId的项
    traceId = common.get("traceId")
    if not traceId in get_ssm():
        raise Exception('traceId not in ssm')

    return True


def lambda_handler(event, context):
    return check_parameter(**event)
    # 1. action.cat 只能是 scenarioTrigger
    # 2. scenarioId 必须存在
    # 3. ssm 中必须存在 key 为 tenantId的项
