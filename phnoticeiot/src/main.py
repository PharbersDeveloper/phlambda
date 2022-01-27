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
        data = finishingEventData(record)
        topic = "pharbers"
        message = json.dumps(data, ensure_ascii=False)
        iot_data_client.publish(topic=topic, qos=2, payload=message)

    # topic = event["topic"]
    # message = event["message"]
    #
    # response = iot_data_client.publish(topic=topic, qos=2, payload=message)
    #
    # return {
    #     "message": "IOT send {message} to topic={topic}".format(message=message, topic=topic),
    #     "response": response
    # }
