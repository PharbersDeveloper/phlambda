import os, sys
import boto3
import logging

from iot.ph_mqtt import PhMQTT


DEFAULT_AWS_ACCESS_KEY = "AKIAWPBDTVEAPUSJJMWN"
DEFAULT_AWS_SECRET_KEY = "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"

DEFAULT_IOT_CA_BUCKET_NAME = "ph-platform"
DEFAULT_IOT_ENDPOINT = "a23ve0kwl75dll-ats.iot.cn-northwest-1.amazonaws.com.cn"
DEFAULT_IOT_CRT_FILE_NAME = "2020-11-11/certificaties/IoT/all/iot-certificate.pem.crt"
DEFAULT_IOT_PK_FILE_NAME = "2020-11-11/certificaties/IoT/all/iot-private.pem.key"
DEFAULT_IOT_CA_FILE_NAME = "2020-11-11/certificaties/IoT/all/root-CA.crt"
DEFAULT_IOT_CLEAN_SESSION = False
DEFAULT_IOT_KEEP_ALIVE = 6


phlogger = logging.getLogger("ph-log")
formatter = logging.Formatter("{ 'Time': %(asctime)s, 'Message': %(message)s, 'File': %(filename)s, 'Func': "
                                      "%(funcName)s, 'Line': %(lineno)s, 'Level': %(levelname)s } ")
sys_handler = logging.StreamHandler(stream=sys.stdout)
sys_handler.setFormatter(formatter)
phlogger.addHandler(sys_handler)
phlogger.setLevel(logging.DEBUG)


def getObject(bucket_name, object_name):
    s3 = boto3.client("s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", DEFAULT_AWS_ACCESS_KEY),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", DEFAULT_AWS_SECRET_KEY),
                region_name="cn-northwest-1")
    return s3.get_object(Bucket=bucket_name, Key=object_name)["Body"].read().decode("utf-8")


iot_ca_bucket_name = os.getenv("IOT_CA_BUCKET_NAME", DEFAULT_IOT_CA_BUCKET_NAME)
ph_mqtt = PhMQTT(
    endpoint = os.getenv("IOT_ENDPOINT", DEFAULT_IOT_ENDPOINT),
    cert = getObject(iot_ca_bucket_name, os.getenv("IOT_CRT_FILE_NAME", DEFAULT_IOT_CRT_FILE_NAME)),
    key = getObject(iot_ca_bucket_name, os.getenv("IOT_PK_FILE_NAME", DEFAULT_IOT_PK_FILE_NAME)),
    ca = getObject(iot_ca_bucket_name, os.getenv("IOT_CA_FILE_NAME", DEFAULT_IOT_CA_FILE_NAME)),
    clean_session = os.getenv("IOT_CLEAN_SESSION", DEFAULT_IOT_CLEAN_SESSION),
    keep_alive = os.getenv("IOT_KEEP_ALIVE", DEFAULT_IOT_KEEP_ALIVE),
)
ph_mqtt.build()
ph_mqtt.open()


def lambda_handler(event, context):
    '''
    event content: 
        {
            "email": "pqian@pharbers.com",
            "subject": "监控",
            "content_type": "text/plain",
            "content": "测试",
            "topic": "test/2",
            "message": "{xx: xx}"
        }
    '''
    phlogger.info("event = " + event)
    phlogger.info("context = " + context)
    phlogger.info("ph_mqtt starting = " + ph_mqtt)

    topic = event['topic']
    message = event['message']

    ph_mqtt.publish(topic, message)
    ph_mqtt.close()

    return { 
        'message': 'IOT send $message to topic=$topic'.format(message=message, topic=topic)
    }


if __name__ == '__main__':
    phlogger.info("__main__")
    test_topic = 'test/1'
    test_message = 'test message'
    
    ph_mqtt.publish(test_topic, test_message)
    ph_mqtt.close()
