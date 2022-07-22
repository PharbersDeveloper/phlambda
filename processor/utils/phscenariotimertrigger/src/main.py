import json
import boto3
import uuid
import time
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


def s3_udepter(Records):
    for record in Records:
        for MessageAttribute in json.loads(record.get("Sns", {}).get("Message", {})).get("Records"):
            s3 = MessageAttribute.get("s3", {})
            bucket = s3.get("bucket", {}).get("name", "")
            key = s3.get("object", {}).get("key", "")
            print(bucket)
            print(key)
            key = key.replace(key[key.rfind("/"):], "")
            name = key.split("/")[-1]
            key = key.replace(name, "")
            print(key)
            s3_client = boto3.client('s3')
            response = s3_client.get_object(Bucket=bucket, Key=key + "__resource.json")
            return json.loads(response.get('Body').read())


def get_uuid():
    uu_id = uuid.uuid4()
    suu_id = ''.join(str(uu_id).split('-'))
    return suu_id


def lambda_handler(event, context):
    print(event)
    traceId = get_uuid()
    Records = event.get("Records", [])
    if Records:
        results = s3_udepter(Records)
        for result in results:
            args = {
                "common": {
                    "tenantId": result["tenantId"],
                    "traceId": traceId,
                    "projectId": result["projectId"],
                    "projectName": result["projectName"],
                    "owner": result["owner"],
                    "showName": result["showName"]
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
                    "scenarioId": result["scenarioId"],
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
            time.sleep(2)

    else:
        # scenario = query_scenario(**event)[0]
        for scenario in query_scenario(**event):
            args = {
                "common": {
                    "tenantId": event["TenantId"],
                    "traceId": traceId,
                    "projectId": event["ProjectId"],
                    "projectName": scenario.get("projectName"),
                    "owner": scenario.get("owner"),
                    "showName": scenario.get("showName")
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
            state_machine_arn = f"arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:scenariotrigger"
            client = boto3.client("stepfunctions")
            res = client.start_execution(stateMachineArn=state_machine_arn,
                                         name=trace_id, input=json.dumps(args, ensure_ascii=False))
            run_arn = res["executionArn"]
            print("Started run %s. ARN is %s.", trace_id, run_arn)

    # ---------------------- 埋点 -------------------------------------#
    aws_cloudwatch_put_metric_data(NameSpace='pharbers-platform',
                                   MetricName='platform-usage',
                                   tenantId=event["TenantId"])
    # ---------------------- 埋点 -------------------------------------#

    return True
