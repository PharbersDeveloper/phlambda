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
        if record["eventName"] != "REMOVE":
            print(record)
            data = finishingEventData(record["dynamodb"]["NewImage"])
            data["jobCat"] = "notification"
            data["jobDesc"] = "executionStatus"
            # [projectId, ownerId] = data["id"].split("_")

            projectId = data["id"][:15]
            ownerId = data["id"][16:]

            topic = f"""{projectId}/{ownerId}/executionStatus"""
            print("Topic =======> \n")
            print(topic)
            message = json.dumps(data, ensure_ascii=False)
            print(message)
            iot_data_client.publish(topic=topic,
                                    qos=1,
                                    retain=False,
                                    payload=message)
