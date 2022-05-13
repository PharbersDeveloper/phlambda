
import boto3
from abc import ABC, abstractmethod


class Logs(ABC):

    def __init__(self):
        self.s3 = boto3.client('s3')

    def get_data(self, bucket, key):
        try:
            response = self.s3.get_object(Bucket=bucket, Key=key)
            return response.get('Body').read()
        except:
            return

    @abstractmethod
    def run(self, **kwargs):
        pass
