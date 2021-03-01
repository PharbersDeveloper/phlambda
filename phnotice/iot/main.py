import os, sys
import boto3
import logging


phlogger = logging.getLogger("ph-log")
formatter = logging.Formatter("{ 'Time': %(asctime)s, 'Message': %(message)s, 'File': %(filename)s, 'Func': "
                                      "%(funcName)s, 'Line': %(lineno)s, 'Level': %(levelname)s } ")
sys_handler = logging.StreamHandler(stream=sys.stdout)
sys_handler.setFormatter(formatter)
phlogger.addHandler(sys_handler)
phlogger.setLevel(logging.DEBUG)


iot_data_client = boto3.client('iot-data', region_name="cn-northwest-1")


def lambda_handler(event, context):
    '''
    event content: 
        {
            "email": "pqian@pharbers.com",
            "subject": "监控",
            "content_type": "text/plain",
            "content": "测试",
            "topic": "test/1",
            "message": "{key: value}"
        }
    '''
    phlogger.info("event = " + str(event))
    phlogger.info("ph_mqtt starting = " + str(iot_data_client))

    topic = event['topic']
    message = event['message']

    response = iot_data_client.publish(topic=topic, payload=message)

    return { 
        'message': 'IOT send {message} to topic={topic}'.format(message=message, topic=topic),
        'response': response
    }


if __name__ == '__main__':
    phlogger.info("__main__")
    topic = 'test/1'
    message = 'test message'
    response = iot_data_client.publish(topic=topic, payload=message)
    print('IOT send {message} to topic={topic}, response={response}'.format(message=message, topic=topic, response=response))