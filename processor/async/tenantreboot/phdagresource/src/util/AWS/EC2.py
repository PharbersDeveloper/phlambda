import json

import boto3
from constants.Common import Common


class EC2(object):

    def __init__(self, **kwargs):
        self.access_key = kwargs.get("access_key", None)
        self.secret_key = kwargs.get("secret_key", None)
        self.ec2_client = boto3.client('ec2')

    def get_volume_id(self, projectId):
        ec2_client = boto3.client('ec2')
        response = ec2_client.describe_volumes()
        for volume in response.get("Volumes"):
            if volume.get("Tags"):
                for tag in volume.get("Tags"):
                    if tag.get("Value") == projectId:
                        volumeId = volume.get("VolumeId")

        return volumeId
