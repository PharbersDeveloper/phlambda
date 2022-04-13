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

    def get_resource_status(self, project_id):
        res = self.ssm.get_ssm_parameter("resource_status")
        status = "closed"
        started_number = 0
        action_id = "default_action_id"
        for resource in res:
            if resource.get("projectId") == project_id:
                status = resource.get("status", "closed")
                action_id = resource.get("actionId", "default_actionId")
            if resource.get("status") == "started" or resource.get("status") == "starting":
                started_number = started_number + 1
        msg = {
            "resource_status": status,
            "action_id": action_id,
            "started_number": started_number
        }
        return msg

    def put_resource_status(self, status, action_id):
        res = self.ssm.get_ssm_parameter("resource_status")
        project_id = self.event.get("projectId")
        for resource in res:
            if resource.get("projectId") == project_id:
                args_index = res.index(resource)
                res.pop(args_index)
        resource = {
            "status": status,
            "actionId": action_id,
            "projectId": self.event.get("projectId")
        }
        res.append(resource)
        self.ssm.put_ssm_parameter("resource_status", json.dumps(res))
        msg = {
            "resource_status": status,
            "action_id": action_id
        }
        return msg

    def insert_action(self, event, operate_type):

        data = {
            "table_name": "action"
        }
        item = {}
        message = {}
        action_id = self.generateId.generate()
        message.update({"projectId": self.event.get("projectId")})
        message.update({"projectName": event.get("projectName")})
        message.update({"owner": event.get("owner")})
        message.update({"showName": event.get("showName")})
        item.update({"id": action_id})
        item.update({"date": str(int(round(time.time() * 1000)))})
        item.update({"projectId": self.event.get("projectId")})
        item.update({"code": 0})
        item.update({"showName": event.get("showName")})
        item.update({"jobDesc": operate_type})
        item.update({"comments": ""})
        item.update({"owner": event.get("owner")})
        item.update({"message": json.dumps(message,  ensure_ascii=False)})
        item.update({"jobCat": operate_type})
        data.update({"item": item})
        self.dynamodb.putData(data)

        return action_id

    def execute(self):
        # 192.168.16.119
        operation_type = self.event.get("operation_type")
        if operation_type == "get_status":
            msg = self.get_status_execute()
        elif operation_type == "operate_resource":
            msg = self.resource_execute()
        return msg

    def get_status_execute(self):
        project_id = self.event.get("projectId")
        msg = self.get_resource_status(project_id)

        return msg

    def resource_execute(self):

        project_id = self.event.get("projectId")
        msg = self.get_resource_status(project_id)
        if self.resource_type == "start" and msg.get("resource_status") == "closed":
            # 创建action 并且 更新ssm
            status = "starting"
            action_id = self.insert_action(self.event, "resource_create")
            msg = self.put_resource_status(status, action_id)
        elif self.resource_type == "close" and msg.get("resource_status") == "started":
            status = "closed"
            action_id = self.insert_action(self.event, "resource_delete")
            msg = self.put_resource_status(status, action_id)

        return msg

