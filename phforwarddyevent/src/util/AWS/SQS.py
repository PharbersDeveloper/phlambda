import boto3
import json
from util.GenerateID import GenerateID

class SQS():

    def __init__(self, **kwargs):

        self.sqs_client = boto3.client('sqs')

    def sqs_send_message(self, message):
        message_group_id = GenerateID().generate()
        print("message id ========================")
        print(message_group_id)
        response = self.sqs_client.send_message(
            QueueUrl="https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph-dyevent-pipeline.fifo",
            MessageBody=json.dumps(message, ensure_ascii=False),
            MessageGroupId=message_group_id
        )
