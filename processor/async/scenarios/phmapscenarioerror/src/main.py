import json
from pherrorlayer import *
import re

'''
event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "scenario.$": "$.scenario",
        "triggers.$": "$.triggers",
        "steps.$": "$.steps",
        "error.$": "$.error"
      }
'''

def ChangeStrToDict(data):
    return json.loads(data) if isinstance(data, str) else data

def FindErrorKey(key):
    Patter = re.compile(pattern='Cause', flags=re.IGNORECASE)
    result = Patter.findall(string=key)
    return True if len(result) > 0 else False

def FindErrorCause(data):
    data = ChangeStrToDict(data)
    try:
        tag = data['errorType']
        return tag
    except Exception as e:
        return False

def SearchErrorType(error):
    keys = ChangeStrToDict(error).keys()
    keys = list(filter(lambda x: FindErrorKey(x) is True, keys))
    if len(keys) == 0:
        return None
    else:
        cause = list(map(lambda x: ChangeStrToDict(error[x]), keys))
        return cause

def MapErrorType(cause):

    if cause is None:
        tmp = serialization(Errors)
    else:
        #1 错误类型
        errorTypes = list(map(lambda x: x.get("errorType"), cause))
        #----解析参数类型--------#
        if "KeyError" in errorTypes:
            tmp = serialization(ParameterError)
        #--- 解析主动抛出的异常内容-----#
        elif "Exception" in errorTypes:
            Errordetails = list(map(lambda x: x.get("errorMessage"), cause))
            print("解析错误内容")
            #TODO 后续类型增多后再采用表驱动的形式来匹配，去掉if else
            if "scenario name already exist" in Errordetails:
                tmp = serialization(ScenarioNameDuplicateError)
            else:
                tmp = serialization(Errors)
        else:
            tmp = serialization(Errors)
    return tmp


#---- 处理抛出的错误信息 -----------#
def lambda_handler(event, context):
    print("*"*50 + " EVENT " + "*"*50)
    print(event)

    error = event["error"]
    print("*"*50 + "传入的 ERROR 信息 " + "*"*50)
    print(error)

    try:
        cause = SearchErrorType(error)
        #---- 基于error信息映射pherrorlayer ----------#
        #TODO 目前对事件错误信息掌握不全，需要多次测试后再编写映射逻辑
        errorMessage = MapErrorType(cause)
    except Exception as e:
        print("*"*50 + "代码异常" + "*"*50, e)
        errorMessage = serialization(Errors)

    result = {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": errorMessage
        }
    }
    print(result)

    return result
