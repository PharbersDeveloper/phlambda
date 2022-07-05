import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from phmetriclayer import aws_cloudwatch_put_metric_data

def query_scenario(ProjectId, ScenarioId, **kwargs):
    print(ProjectId)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('scenario')
    res = table.query(
        KeyConditionExpression=Key("projectId").eq(ProjectId) & Key('id').eq(ScenarioId),
    )
    return res["Items"]


def lambda_handler(event, context):
    print(event)
    scenario = query_scenario(**event)[0]

    args = {
        "common": {
            "tenantId": event["TenantId"],
            "traceId": scenario["traceId"],
            "projectId": event["ProjectId"],
            "projectName": scenario["projectName"],
            "owner": scenario["owner"],
            "showName": scenario["showName"]
        },
        "action": {
            "cat": "scenarioTrigger",
            "desc": "scenarioTrigger",
            "comments": "",
            "message": "",
            "required": True
        },
        "notification": {
            "required": True
        },
        "scenario": {
            "scenarioId": event["ScenarioId"],
            "runtime": "timer"
        }
    }

    trace_id = args["common"]["traceId"]
    state_machine_arn = f"arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:scenario-trigger"
    client = boto3.client("stepfunctions")
    res = client.start_execution(stateMachineArn=state_machine_arn,
                                 name=trace_id, input=json.dumps(args, ensure_ascii=False))
    run_arn = res["executionArn"]
    print("Started run %s. ARN is %s.", trace_id, run_arn)

    #---------------------- 埋点 -------------------------------------#
    aws_cloudwatch_put_metric_data(NameSpace='pharbers-platform',
                                   MetricName='platform-usage',
                                   tenantId=args["common"]["tenantId"])
    #---------------------- 埋点 -------------------------------------#


    return True
