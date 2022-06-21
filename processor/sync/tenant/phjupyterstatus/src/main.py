import json
import boto3
import traceback
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
client = boto3.client('cloudformation')
ssm = boto3.client('ssm')

'''
1. 看stack 在不在 
    1.1 stackname 的获取方法是 在dynamodb中找到resource 表中 tenantid 下的所有 ownership 为 shared 值的 
    1.2 对每一个值中的property 遍历，形成一个stackname 的数组
    1.3 stackname 的名字规则为  <role>-<property.type>-<tenantId>
    1.4 所有的stak 在cloud formation 中都不存在 算过，要不然报错，说哪一个 stack 指向的role 以及type 存在
       
2. ssm 是否存在，如果存在，报错，不能重复创建并提交管理员

event = {
    "tenantId": "12345"
}

return = {
    "status": Number [ 0: stoped , 1: starting , 2: started , 4: stoping ]
    "message": String
    "traceId": String
}
'''


def resourceCheck(stackNameList):
    '''
    check resouce stack name
    & operator
    @param resouce: check item
    @return: 
        0: stoped
        1: starting 
        2: started
        4: stoping
    '''

    result = 0
    for stackName in stackNameList:
        try:
            response = client.describe_stacks(StackName=stackName)["Stacks"]
        except:
            traceback.print_exc()
            print("{} is stoped".format(stackName))
            response = []
        finally:
            if len(response) == 0:
                print("{} is stoped".format(stackName))
                result |= 0
            elif len(response) == 1 and response[0]["StackStatus"] in ["CREATE_IN_PROGRESS", "UPDATE_IN_PROGRESS"]:
                print("{} is starting".format(stackName))
                result |=1
            elif len(response) == 1 and response[0]["StackStatus"] in ["CREATE_COMPLETE", "UPDATE_COMPLETE"]:
                print("{} is started".format(stackName))
                result |= 2
            elif len(response) == 1 and response[0]["StackStatus"] in ["DELETE_IN_PROGRESS"]:
                print("{} is stoping".format(stackName))
                result |= 4
            else:
                raise Exception("unexcept status ({}) for {}".format(response[0]["StackStatus"], stackName))

    return result


def ssmCheck(ssmNameList):
    '''
    @return: 
        0: stoped
        2: started
    '''
    result = 0
    for ssmName in ssmNameList:
        ssmName = ssmName.replace("=", "-")
        try:
            response = client.get_parameter(
                Name=ssmName
            )
            print(response)
            result |= 2
        except:
            result |= 0
    return result


def ssmQueryTraceId(ssm_name):
    '''
    @return: traceId
    '''
    print(ssm_name)
    response = ssm.get_parameter(
        Name=ssm_name
    )
    print(response)
    value = json.loads(response["Parameter"]["Value"])
    return value["traceId"]
    

def errorMessage(e):
    message = {
        "status": -99,
        "message": json.dumps(str(e)),
        "traceId": ""
    }
    return message


def list_cloudformation_ssm_name(resource, resourceId):
    stackNameList = []
    ssmNameList = []
    properties = json.loads(resource["properties"])
    for prop in properties:
        stackName = "-".join([resource["role"], prop["type"], resource["tenantId"], resource["ownership"],
                              resource["owner"]]).replace("_", "-").replace(":", "-").replace("+", "-")

        ssmName = '-'.join([prop['type'], resource['owner'], resourceId]).replace("=", "-")
        stackNameList.append(stackName)
        ssmNameList.append(ssmName)
    return stackNameList, ssmNameList


def query_status(tenantId, resourceId):
    result = {
        "status": -99,
        "message": "",
        "traceId": "",
        "id": resourceId
    }
    table = dynamodb.Table('resource')
    res = table.query(
        KeyConditionExpression=Key("tenantId").eq(tenantId),
        FilterExpression=Attr("ownership").eq("personal")
    )
    resources = res["Items"]
    print(resources)

    statusCode = 0
    for item in resources:
        stackNameList, ssmNameList = list_cloudformation_ssm_name(item, resourceId)
        statusCode |= resourceCheck(stackNameList)
        statusCode |= ssmCheck(ssmNameList)

    print(statusCode)
    if (statusCode & 4) != 0:
        result["status"] = 4
        result["message"] = "stoping"
        result["traceId"] = ssmQueryTraceId(ssmNameList[0])
    elif (statusCode & 1) != 0:
        result["status"] = 1
        result["message"] = "starting"
        result["traceId"] = ssmQueryTraceId(ssmNameList[0])
    elif (statusCode & 2) != 0:
        result["status"] = 2
        result["message"] = "started"
        result["traceId"] = ssmQueryTraceId(ssmNameList[0])
    elif statusCode == 0:
        result["status"] = 0
        result["message"] = "stoped"
        result["traceId"] = ""
    else:
        raise Exception("unknown error")
    return result


def lambda_handler(event, context):
    event = json.loads(event["body"])
    print(event)
    code = 200
    status = 0
    result = []
    resourceIds = event["resourceIds"]
    tenantId = event["tenantId"]

    for resourceId in resourceIds:
        try:
            resource_status = query_status(tenantId, resourceId)

        except Exception as e:
            # printing stack trace
            traceback.print_exc()
            resource_status = errorMessage(e)
            resource_status["id"] = resourceId
        result.append(resource_status)

    return {
        "statusCode": code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps({"status": "ok", "error": "null", "data": result})
}
