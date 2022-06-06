import os
import json
import boto3
import traceback
from boto3.dynamodb.conditions import Key

# TODO: ... 在这里看是否能创建。这个地方也会是创建流程的唯一入口

# 1. stack 是否存在，如果存在 报错，不能重复创建
#     1.1 stackname 的获取方法是 在dynamodb中找到resource 根据resource id 找到需要创建的项
#     1.2 对每一个值中的property 遍历，形成一个stackname 的数组
#     1.3 stackname 的名字规则为  <role>-<property.type>-<tenantId>-<ownership>-<owner>
#     1.4 所有的stak 在cloud formation 中都不存在 算过，要不然报错，说哪一个 stack 指向的role 以及type 存在
# 2. ssm 是否存在，如果存在，报错，不能重复创建并提交管理员
# @mzhang


class SolveStackName:

    def query_resource_item(self, tableName, ValueOfPartitionKey, ValueOfSortKey):
        dynamobd = boto3.resource('dynamodb')
        ds_table = dynamobd.Table(tableName)
        resp = ds_table.query(
            KeyConditionExpression=Key('tenantId').eq(ValueOfPartitionKey)
                                   & Key('id').eq(ValueOfSortKey)
        )

        return resp['Items']

    def generate_stackName_by_ResourceItem(self, ItemOfResource):
        stackNameList = []
        for elem in ItemOfResource:
            properties = elem['properties']
            properties = (json.loads(properties) if isinstance(properties, str) else properties)[0]
            # 1.3 stackname 的名字规则为  <role>-<property.type>-<tenantId>-<ownership>-<owner>
            stackName = '-'.join([elem['role'], properties['type'], elem['tenantId'], elem['ownership'], elem['owner']])
            stackNameList.append(stackName)
        return stackNameList

    def IsCloudFomationContainStackName(self, stackNameList):
        #1.4 所有的stak 在cloud formation 中都不存在 算过，要不然报错，说哪一个 stack 指向的role 以及type 存在
        for stackName in stackNameList:
            print(stackName)
            self.getStackExisted(stackName)

    def getStackExisted(self, stackName):
        cf = boto3.client('cloudformation', region_name='cn-northwest-1', aws_access_key_id='AKIAWPBDTVEANKEW2XNC', aws_secret_access_key='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')
        try:
            stacks = cf.describe_stacks(StackName=stackName)
            if len(stacks) > 0:
                raise Exception(f"{stackName} already exist")
        except Exception as e:
            import re
            ExistPattern = ".*?(already exist)"
            NotExistPattern = "An error occurred \(ValidationError\) when calling the DescribeStacks operation:.*?(does not exist)"
            findExistResult = re.findall(pattern=ExistPattern, string=str(e))
            findNotXistResult = re.findall(pattern=NotExistPattern, string=str(e))
            #-----------stack not exist --------------------------------#
            if len(findExistResult) > 0 and findExistResult[0] == "already exist":
                #role = stackName.split('-')[0]
                #type = stackName.split('-')[1]
                raise Exception(f"{stackName} already exist")
            #--------stack not exist -------------------------------------#
            elif len(findNotXistResult) > 0 and findNotXistResult[0] == "does not exist":
                pass
            else:
                raise Exception(f"unkown error: {str(e)}")

    def IsSSMExist(self, stackNameList, resourceId):
        for elem in stackNameList:
            data_all = elem.split('-')
            typeName, owner = data_all[1], data_all[-1]
            ssmName = self.get_SSMName(typeName, owner, resourceId)
            self.checkSSMExist(ssmName)

    #currentStep.type, $.common.owner, $.resourceId
    def get_SSMName(self, typeName, owner, resourceId):
        return '-'.join([typeName, owner, resourceId])

    #-------------------ssm 是否存在，如果存在，报错，不能重复创建并提交管理员 -------------------#
    def checkSSMExist(self, ssmName):
        client = boto3.client('ssm')
        try:
            response = client.describe_association(
                Name=ssmName,
            )
            print(response)
        except Exception as e:
            print(e)

def lambda_handler(event, context):
    event = json.loads(event["body"])
    print(event)
    resourceId = "mIMzFAKEyU6JBc7nl1NmBA=="
    trace_id = "alfredtest"
    #trace_id = event["traceId"]

    #--------- 数据验证 --------------------------------#
    stackClient = SolveStackName()
    Items = stackClient.query_resource_item('resource', trace_id, resourceId)
    stackNameList = stackClient.generate_stackName_by_ResourceItem(Items)
    stackClient.IsCloudFomationContainStackName(stackNameList)
    stackClient.IsSSMExist(stackNameList, resourceId)
    #--------- 数据验证 --------------------------------#

    result = {
        "status": "",
        "message": "",
        "trace_id": "",
        "resourceId": "",
    }
    # trace_id = ""
    # edition = "" if os.getenv("EDITION") == "V2" else "-dev"
    # traceId = event.get("common").get("traceId")
    # 1. event to args
    args = {
        "common": {
            "tenantId": event["tenantId"],
            "traceId": trace_id,
            "projectId": "ggjpDje0HUC2JW",
            "projectName": "demo",
            "owner": event["owner"],
            "showName": event["showName"]
        },
        "action": {
            "cat": "personalres-boot",
            "desc": "reboot project",
            "comments": "something need to say",
            "message": "something need to say",
            "required": True
        },
        "resourcesId": resourceId,  # TODO: 从 event 中找到 resourceID @mzhang
        "notification": {
            "required": True
        }   
    }

    try:
        trace_id = args["common"]["traceId"]
        # state_machine_arn = os.environ["ARN"]
        state_machine_arn = f"arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:personal-res-boot"
        client = boto3.client("stepfunctions")
        res = client.start_execution(stateMachineArn=state_machine_arn, #+ edition,
                                     name=trace_id, input=json.dumps(args, ensure_ascii=False))
        run_arn = res["executionArn"]
        print("Started run %s. ARN is %s.", trace_id, run_arn)
        result["status"] = "succeed"
        result["message"] = "start run " + trace_id
        result["trace_id"] = trace_id

    except Exception:
        result["status"] = "failed"
        result["message"] = "Couldn't start run " + trace_id
        result["trace_id"] = trace_id

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(result)
    }

