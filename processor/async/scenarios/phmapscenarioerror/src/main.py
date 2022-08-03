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
        cause = list(filter(lambda x: FindErrorCause(error[x]) is not False, keys))
        cause = list(map(lambda x: FindErrorCause(ChangeStrToDict(error[x])), cause))
        if len(cause) == 0:
            return None
        return cause

def MapErrorType(cause):

    if cause is None:
        tmp = serialization(Errors)
    else:
        #--- 错误详情，用于解析映射用 -----#
        ErrorKeys = list(*map(lambda x: list(x.keys()), cause))
        if "KeyError" in ErrorKeys:
            tmp = serialization(ParameterError)
        #TODO 后续出现新的错误类型再添加
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

    cause = SearchErrorType(error)


    #---- 基于error信息映射pherrorlayer ----------#
    #TODO 目前对事件错误信息掌握不全，需要多次测试后再编写映射逻辑
    errorMessage = MapErrorType(cause)

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


#-- 本地测试用 --#
if __name__ == '__main__':

    event = {'traceId': '569abb059b0940a68f21f3erw24b060df77', 'owner': '35cca7e1-45d9-4a6e-80f6-09e5417feb33', 'showName': '朗轩齐', 'scenario': {'id': 'ggjpDje0HUC2JW_5c689d48746846958cb62582a3f46qwer083', 'active': True, 'scenarioName': '00000', 'deletion': False}, 'projectName': 'demo', 'triggers': [], 'error': {'Error': 'KeyError', 'Cause': '{"errorMessage": "\'index\'", "errorType": "KeyError", "stackTrace": ["  File \\"/var/task/main.py\\", line 119, in lambda_handler\\n    scenarioClient.put_item()\\n", "  File \\"/var/task/main.py\\", line 71, in put_item\\n    \'index\': self.turn_decimal_into_int(self.get_index()),\\n", "  File \\"/var/task/main.py\\", line 42, in get_index\\n    return self.scenario[\'index\']\\n"]}'}, 'projectId': 'ggjpDje0HeqrewUC2JW', 'steps': []}
    lambda_handler(event,"")








