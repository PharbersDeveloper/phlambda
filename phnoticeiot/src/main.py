import os, sys
import json
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
    need event content: 
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

    if 'Records' in event:
        records = event['Records'][0]
        if 'EventSource' in records and records['EventSource'] == 'aws:sns':
            message = records['Sns']['Message']
            event = json.loads(message)
    phlogger.info("actual_event = " + str(event))

    topic = event['topic']
    message = event['message']

    response = iot_data_client.publish(topic=topic, payload=message)

    return { 
        'message': 'IOT send {message} to topic={topic}'.format(message=message, topic=topic),
        'response': response
    }


if __name__ == '__main__':
    # phlogger.info("__main__")
    # topic = 'test/1'
    # message = 'test message'
    # response = iot_data_client.publish(topic=topic, payload=message)
    # print('IOT send {message} to topic={topic}, response={response}'.format(message=message, topic=topic, response=response))
    event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws-cn:sns:cn-northwest-1:444603803904:PH_NOTICE_IOT:c5405122-d1b8-4aad-b344-c7971bf436b9', 'Sns': {'Type': 'Notification', 'MessageId': 'da5269bd-8888-5fb8-bf30-310b41529fc4', 'TopicArn': 'arn:aws-cn:sns:cn-northwest-1:444603803904:PH_NOTICE_IOT', 'Subject': None, 'Message': '{\n  "email": "pqian@pharbers.com",\n  "subject": "监控",\n  "content_type": "text/plain",\n  "content": "测试",\n  "topic": "test/1",\n  "message": "{key: value}"\n}', 'Timestamp': '2021-03-01T10:53:14.540Z', 'SignatureVersion': '1', 'Signature': 'vm/EPvwntxzAz/VbvdBBHrsttYaajf5HF4w5HRoJGlREmjlp4AjQhhZAAaVGdKILNHjXpm4b3v1qMjolCW06a7Gk2K1TBWwGte+5vpUHvu8QI7Fy9duHDyrRzoIu+G80IHj6GmJWgM4+M+ZsWtXjH/UUnqdRIBTsIL6Zhr8qXAeOlSjQxAIWpZ02KYluqGPCWe6UAc5FxUXE19BIQF+atzhoh4ZyXYeKK4ofK2ynjmQAEwthvqoMfHrMmBHL5Iqi4qwiZ2Np0A3oy1pt64guzQ7uzQyhemRMlli27iDyXC07iwFtGjvcsFb8ZafKfyN8KP2HMLd1QyNNH+jKI611lg==', 'SigningCertUrl': 'https://sns.cn-northwest-1.amazonaws.com.cn/SimpleNotificationService-0749073bc68bdbbdbbf22cdd192ab3f3.pem', 'UnsubscribeUrl': 'https://sns.cn-northwest-1.amazonaws.com.cn/?Action=Unsubscribe&SubscriptionArn=arn:aws-cn:sns:cn-northwest-1:444603803904:PH_NOTICE_IOT:c5405122-d1b8-4aad-b344-c7971bf436b9', 'MessageAttributes': {}}}]}
