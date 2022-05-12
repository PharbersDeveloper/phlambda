import json
import boto3
from boto3.dynamodb.conditions import Attr
from datetime import datetime

'''
这个函数只做两件事情，
# 1. 将所有的错误都提取出来写入到notification中
2. 将创建成功但整体失败的东西会滚

args:
    event = {
        "common": {
            "traceId": "alfred-resource-creation-traceId",
            "projectId": "ggjpDje0HUC2JW",
            "projectName": "demo",
            "owner": "alfred",
            "showName": "alfred"
        },
        "action": {
            "cat": "createOrUpdateScenario",
            "desc": "create or update scenario",
            "comments": "something need to say",
            "message": "something need to say",
            "required": true
        },
        "notification": {
            "required": true      
        },
        "scenario": {
            "id": "scenario id",       # 如果有就是update，如果没有就是新建
            "active": true,
            "scenarioName": "scenario name",
            "deletion": true | false      # 如果是true，则所有和scenario相关的全部删除
        },
        "triggers": [
            {
                "active": true,
                "detail": {
                    "timezone":"中国北京",
                    "start":"2022-04-26 16:10:14",
                    "period":"minute",
                    "value":1
                },
                "index": 0,
                "mode": "timer",
                "id": "trigger id",       # 如果有就是update，如果没有就是新建
            }
        ],
        "steps": [
            {
                "confData": {},
                "detail": {
                    "type":"dataset",
                    "recursive":false,
                    "ignore-error":false,
                    "name":"1235"
                },
                "index": 0,
                "mode": "dataset",,
                "name": "alfred"
                "id": "step id",       # 如果有就是update，如果没有就是新建
            }
        ],
        "error": {
            "Error": "Exception",
            "Cause": ""
        }
    }
'''
def ExtractToNotification(id, projectId,category, code, comments, date, jobCat, jobDesc, message, owner, showName, status,traceId):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('notification')
        response = table.put_item(
            Item={
                'id': id,
                'projectId': projectId,
                'category': category,
                'code': code,
                'comments': comments,
                'date': date,
                'jobCat': jobCat,
                'jobDesc': jobDesc,
                'message': message,
                'owner': owner,
                'showName': showName,
                'status': status,
                'traceId':traceId
            }
        )
        return response

class TriggerRollBack:
    def del_trigger_resource(self,stackName):
        result = {}
        client = boto3.client('cloudformation')
        response = client.delete_stack(
            StackName=stackName    # event['runnerId']
        )
        print(response)
        result['status'] = 'ok'
        result['message'] = 'delete resource success'
        return result


    def del_trigger_item(self, table_name, scenarioId, col_name, col_value):
        dynamodb = boto3.resource("dynamodb", region_name="cn-northwest-1")
        table = dynamodb.Table(table_name)
        table.delete_item(
            Key={
                col_name: col_value,
                "scenarioId": scenarioId
            }
        )


def lambda_handler(event, context):

    #-------------写入notification字段-----------------#
    id = '',     #---目前在表中查到的字段有下列字段，具体对应规则待确认
    projectId =event['common']['projectId'] ,
    category = '',
    code = '',
    comments = event['action']['comments'],
    date = datetime.now().timestamp(),
    jobCat = event['action']['cat'],
    jobDesc = event['action']['desc'],
    message = event['action']['message'],
    owner = event['common']['owner'],
    showName = event['common']['showName'],
    status = '',
    traceId = event['common']['traceId']

    error = event['error']
    #--------------------写入notification表-----------------------#
    ExtractToNotification(id, projectId,category, code, comments, date, jobCat, jobDesc, message, owner, showName, status,traceId)

    #-------------------回滚操作-----------------------------------#
    scenarioId = event['scenario']['id']
    triggers_id = event['triggers']['id']
    stackName = "-".join(["scenario", projectId, scenarioId, triggerId])   #---stackName 存在问题，当操作为update时，stackName不满足此拼接规则，则无法进行资源删除

    TriggerRollBack().del_trigger_item("scenario_trigger", scenarioId, "id", triggers_id)
    result = TriggerRollBack().del_trigger_resource(stackName)

    return result
