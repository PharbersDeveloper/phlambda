import boto3
from util.AWS.PhAWS import PhAWS


class SNS(PhAWS):

    def __init__(self, **kwargs):

        self.sns_client = boto3.client('sns')

    def sns_publish(self, topic_arn, message):
        response = self.sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
        )
