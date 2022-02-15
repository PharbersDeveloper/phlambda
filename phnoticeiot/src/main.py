import json
import boto3


iot_data_client = boto3.client("iot-data", region_name="cn-northwest-1")


def finishingEventData(record):
    item = {}

    for field in list(record.keys()):
        value = record[field]
        v_k = list(value.keys())[0]
        item[field] = value[v_k]
    return item


def lambda_handler(event, context):
    records = event["Records"]
    for record in records:
        data = finishingEventData(record["dynamodb"]["NewImage"])
        projectId = data["projectId"]
        ownerId = json.loads(data["message"])["opname"]
        topic = f"""{projectId}/{ownerId}"""
        message = json.dumps(data, ensure_ascii=False)
        print(message)
        iot_data_client.publish(topic=topic,
                                qos=1,
                                retain=False,
                                payload=message)
