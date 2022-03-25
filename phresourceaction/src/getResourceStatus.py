import re
import subprocess
import os
import time
import json
from util.AWS.SSM import SSM
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID


class GetResourceStatus(object):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.ssm = SSM()
        self.dynamodb = DynamoDB()
        self.generateId = GenerateID()

    def name_convert_to_camel(self, name):
        return re.sub(r'(_[a-z])', lambda x: x.group(1)[1], name.lower())

    def get_resource_status(self, target_name):
        res = self.ssm.get_ssm_parameter("resource_status")
        status = res.get(target_name, "closed")
        return status

    def put_resource_status(self, status):
        res = self.ssm.get_ssm_parameter("resource_status")
        target_name = self.name_convert_to_camel(self.event.get("projectName"))
        res.update({target_name: status})
        self.ssm.put_ssm_parameter("resource_status", json.dumps(res))

    def insert_action(self, event, operate_type):

        data = {
            "table_name": "action"
        }
        item = {}
        message = {}
        message.update({"projectId": self.event.get("projectId")})
        message.update({"projectName": event.get("projectName")})
        message.update({"owner": event.get("owner")})
        message.update({"showName": event.get("showName")})
        item.update({"id": self.generateId.generate()})
        item.update({"date": str(int(round(time.time() * 1000)))})
        item.update({"projectId": self.event.get("projectId")})
        item.update({"code": 0})
        item.update({"showName": event.get("showName")})
        item.update({"jobDesc": "created"})
        item.update({"comments": ""})
        item.update({"owner": event.get("owner")})
        item.update({"message": json.dumps(message,  ensure_ascii=False)})

        item.update({"jobCat": operate_type})
        data.update({"item": item})
        self.dynamodb.putData(data)

    def execute(self):
        # 192.168.16.119
        operation_type= self.event.get("operation_type")
        if operation_type == "get_status":
            status = self.get_status_execute()
        elif operation_type == "operate_resource":
            status = self.resource_execute()
        return status

    def get_status_execute(self):
        project_name = self.event.get("projectName")
        target_name = self.name_convert_to_camel(project_name)
        status = self.get_resource_status(target_name)

        return status

    def resource_execute(self):

        project_name = self.event.get("projectName")
        target_name = self.name_convert_to_camel(project_name)
        status = self.get_resource_status(target_name)
        if self.resource_type == "start" and status == "closed":
            # 创建action 并且 更新ssm
            status = "starting"
            self.insert_action(self.event, "resource_create")
            self.put_resource_status(status)
        elif self.resource_type == "close" and status == "started":
            status = "closed"
            self.insert_action(self.event, "resource_delete")
            self.put_resource_status(status)

        return status

