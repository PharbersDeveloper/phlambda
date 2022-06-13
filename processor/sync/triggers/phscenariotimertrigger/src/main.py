

import json
import boto3


def lambda_handler(event, context):
    event = json.loads(event["body"])
    print(event)
    tenantId = event["tenantId"]

    # args = {
    #     "common": {
    #         "tenantId": tenantId,
    #         "traceId": event["traceId"],
    #         "projectId": "ggjpDje0HUC2JW",
    #         "projectName": "demo",
    #         "owner": event["owner"],
    #         "showName": event["showName"]
    #     },
    #     "action": {
    #         "cat": "personalResBoots",
    #         "desc": "reboot project",
    #         "comments": "something need to say",
    #         "message": "something need to say",
    #         "required": True
    #     },
    #     "notification": {
    #         "required": True
    #     },
    #     "scenario": {
    #         "scenarioId": "ggjpDje0HUC2JW_46c4fd03c44344f68f6848c6eb7cdab8",
    #         "runtime": "manual"
    #     }
    # }

    trace_id = event["common"]["traceId"]
    state_machine_arn = f"arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:scenario-trigger"
    client = boto3.client("stepfunctions")
    res = client.start_execution(stateMachineArn=state_machine_arn, #+ edition,
                                 name=trace_id, input=json.dumps(event, ensure_ascii=False))
    run_arn = res["executionArn"]
    print("Started run %s. ARN is %s.", trace_id, run_arn)

    return True
