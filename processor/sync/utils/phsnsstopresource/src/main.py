import boto3
from stopJupyter import StopJupyter


COMMANDS = {
    'jupyter': StopJupyter,
}


cloudwatch = boto3.client("cloudwatch")

def lambda_handler(event, context):
    # Records = event.get("Records", [])
    # for record in Records:
    #     MessageAttributes = record.get("Sns", {}).get("MessageAttributes", {})
    #     tenantId = MessageAttributes.get("tenantId", {}).get("Value", "")
    #     ctype = MessageAttributes.get("ctype", {}).get("Value", "")
    response = cloudwatch.describe_alarms(AlarmNamePrefix='platform-usage')
    tenantId = ''
    for dimensions in [metricalarm.get("Dimensions") for metricalarm in response.get("MetricAlarms") if metricalarm.get("StateValue") == "ALARM"]:
        for dimen in dimensions:
            if dimen.get("Name") == 'tenantId':
                tenantId = dimen.get("Value")
    if tenantId:
        StopJupyter().run(tenantId)
    return True
