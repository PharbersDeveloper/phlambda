import os
import json
import boto3
import traceback
from boto3.dynamodb.conditions import Key


class SSMAndCloudFormationState:

    def query_resource_item(self, tableName, ValueOfPartitionKey, ValueOfSortKey):
        dynamobd = boto3.resource('dynamodb')
        ds_table = dynamobd.Table(tableName)
        resp = ds_table.query(
            KeyConditionExpression=Key('tenantId').eq(ValueOfPartitionKey)
                                   & Key('id').eq(ValueOfSortKey)
        )

        return resp['Items']

    def generate_stackNameAndSSMName_by_ResourceItem(self, ItemOfResource, resourceId):
        stackNameAndSSMNameList = []
        for elem in ItemOfResource:
            properties = elem['properties']
            properties = (json.loads(properties) if isinstance(properties, str) else properties)[0]
            # 1.3 stackname 的名字规则为  <role>-<property.type>-<tenantId>-<ownership>-<owner>
            stackName = '-'.join([elem['role'], properties['type'], elem['tenantId'], elem['ownership'], elem['owner']])
            ssmName = '-'.join([properties['type'], elem['owner'], resourceId])
            stackNameAndSSMNameList.append((stackName, ssmName))
        return stackNameAndSSMNameList

    def IsStackNameAndSSMNameExist(self, stackNameAndSSMNameList):
        for stackName, ssmName in stackNameAndSSMNameList:
            stackTag = self.checkStackExisted(stackName)
            ssmTag = self.checkSSMExist(ssmName)
            if any([stackTag, ssmTag]) is False:
                errorMessage = stackName if stackTag is False else " " + ssmName if ssmTag is False else " "
                raise Exception(f"{errorMessage} not exist")


    def checkStackExisted(self, stackName):
        cf = boto3.client('cloudformation')
        try:
            stacks = cf.describe_stacks(StackName=stackName)
            if len(stacks) > 0:
                return True
        except Exception as e:
            print(str(e))
            return False

    def checkSSMExist(self, ssmName):
        client = boto3.client('ssm')
        try:
            response = client.describe_association(
                Name=ssmName,
            )
            return True
        except Exception as e:
            print(e)
            return False

def lambda_handler(event, context):
    event = json.loads(event["body"])
    print(event)

    #--------- input args ---------------#
    resourceId = event["resourceId"]
    tenantId = event["tenantId"]
    traceId = event["traceId"]
    owner = event["owner"]
    showName = event["showName"]
    #--------- input args ---------------#

    result = {
        "status": "",
        "message": "",
        "trace_id": "",
        "resouceId": ""
    }
    # trace_id = ""
    # edition = "" if os.getenv("EDITION") == "V2" else "-dev"
    # traceId = event.get("common").get("traceId")

    # TODO: 缺判断当前这个是否已经启动 @mzhang
   #------------判断启动----------------------#
    client = SSMAndCloudFormationState()
    Items = client.query_resource_item('resource', tenantId, resourceId)
    stackNameAndSSMNameList = client.generate_stackNameAndSSMName_by_ResourceItem(Items, resourceId)
    try:
        client.IsStackNameAndSSMNameExist(stackNameAndSSMNameList)
    except Exception as e:
        result["status"] = "failed"
        result["message"] = json.dumps(str(e))
        result["trace_id"] = traceId
    #------------判断启动----------------------#


    # 1. event to args
    args = {
        "common": {
            "tenantId": tenantId,
            "traceId": traceId,
            "projectId": "ggjpDje0HUC2JW",
            "projectName": "demo",
            "owner": owner,
            "showName": showName
        },
        "action": {
            "cat": "tenant-boot",
            "desc": "reboot project",
            "comments": "something need to say",
            "message": "something need to say",
            "required": True
        },
        "resourcesId": resourceId,
        "notification": {
            "required": True
        }   
    }

    try:
        trace_id = args["common"]["traceId"]
        # state_machine_arn = os.environ["ARN"]
        state_machine_arn = f"arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:personal-res-terminate"
        client = boto3.client("stepfunctions")
        res = client.start_execution(stateMachineArn=state_machine_arn, #+edition,
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
