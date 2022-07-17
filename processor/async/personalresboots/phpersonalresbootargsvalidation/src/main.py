import json
import boto3

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
        "cat": "personalResBoots",
        "desc": "reboot jupyter",
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

def check_ssm(tenantId):
    ssm = boto3.client('ssm')
    try:
        response = ssm.get_parameter(
            Name=tenantId
        )
    except:
        raise Exception(f"ssm not exits tenantId: {tenantId}")


def check_parameter(common, action, resourceId=None, **kwargs):

    if not action.get("cat") == "personalResBoots":
        raise Exception('action.cat must be personalResBoots')

    # 2. resourcesId 必须存在
    if not resourceId:
        raise Exception('resourcesId not exits')

    # 3. ssm 中必须存在 key 为 tenantId的项
    tenantId = common.get("tenantId")
    check_ssm(tenantId)

    return True


def lambda_handler(event, context):
    print(event)
    return check_parameter(**event)
    # 1. action.cat 只能是 personalResBoots
    # 2. resourcesId 必须存在
    # 3. ssm 中必须存在 key 为 tenantId的项
