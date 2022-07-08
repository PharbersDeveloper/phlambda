
from s3event import dataset
from timer import timer
import os

'''
这个函数只做一件事情，通过比较更新的内容，查看是否需要创建cf 来更新 timer资源
args:
    event = {
        "tenantId.$":"$.common.tenantId",
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "scenario.$": {
            "id": "scenario id",
            "active": true,
            "scenarioName": "scenario name",
            "deletion": false
        },
        "triggers": [
            {
                "active": true,
                "detail": {
                    "timezone":"中国北京",
                    "start":"2022-04-26 16:10:14",
                    "period":"minute",
                    "value":1
                    "cron":""
                },
                "index": 0,
                "mode": "timer",
                "id": "trigger id"
                "oldimage": {
                    "active": true,
                    "detail": {
                        "timezone":"中国北京",
                        "start":"2022-04-26 16:10:14",
                        "period":"minute",
                        "value":1
                    },
                    "index": 0,
                    "mode": "timer",
                    "id": "trigger id"
                }
            }
        ]
    }
'''


Command ={
    "timer": timer,
    "dataset": dataset,
}


def lambda_handler(event, context):
    print("*"*50 + " event " + "*"*50)
    print(event)

    global tenantId
    global targetArn
    global projectId
    tenantId = event['tenantId']
    targetArn = os.getenv("TARGETARN")
    projectId = event['projectId']
    messageList = []

    if len(event['triggers']) == 0:
        result = {}
        result['status'] = 'error'
        result['message'] = 'triggers is not exists, can not create any resources.'
        #return result
        return {"type": "notification", "opname": event['owner'],
                       "cnotification": {"data": {"datasets": "", "error": result}}}
    else:
        #---------- 处理每一个trigger ------------------------------#
        for trigger in event["triggers"]:
            mode = trigger.get("mode")
            messageList.append(Command[mode](trigger))

        return {"type": "notification", "opname": event['owner'],
                "cnotification": {"data": {"datasets": "", "error": messageList}}}