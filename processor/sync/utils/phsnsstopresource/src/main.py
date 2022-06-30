from stopJupyter import StopJupyter


COMMANDS = {
    'jupyter': StopJupyter,
}


def lambda_handler(event, context):
    Records = event.get("Records", [])
    for record in Records:
        MessageAttributes = record.get("Sns", {}).get("MessageAttributes", {})
        tenantId = MessageAttributes.get("tenantId", {}).get("Value", "")
        ctype = MessageAttributes.get("ctype", {}).get("Value", "")
        COMMANDS[ctype].run(tenantId, ctype)
    return True
