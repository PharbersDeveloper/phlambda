import time
import json
import re
import requests
from phResource.command import Command
from util.AWS.DynamoDB import DynamoDB
from util.AWS.SSM import SSM
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL
from util.GenerateID import GenerateID


class CommandPutNotification(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.target_name = self.name_convert_to_camel(self.project_message.get("projectName"))
        self.project_id = self.project_message.get("projectId")
        self.dynamodb = DynamoDB()
        self.ssm = SSM()

    def name_convert_to_camel(self, name):
        return re.sub(r'(_[a-z])', lambda x: x.group(1)[1], name.lower())

    def airflow_status(self):

        url = "https://"+ self.project_id +".pharbers.com/airflow/api/v1/dags/default_dag_default_dag_developer"
        payload={}
        headers = {
            'Cookie': 'AWSALBTG=4OrpUZOfa1M47ma2ZbTf3+hF+G9KxGadugIRMRgf0hp9lTl3XoBpx787sMy9kcswdrSRPyqVHZJSG5z7wwVbIxsWq1oMVZSLenr3lwdtAD72QjFmCipiSQCHaCT7uPWA8YD0CXkvbiigcCopsqFsGOgzxt2P+/S6Y97s89fipQ4B; AWSALBTGCORS=4OrpUZOfa1M47ma2ZbTf3+hF+G9KxGadugIRMRgf0hp9lTl3XoBpx787sMy9kcswdrSRPyqVHZJSG5z7wwVbIxsWq1oMVZSLenr3lwdtAD72QjFmCipiSQCHaCT7uPWA8YD0CXkvbiigcCopsqFsGOgzxt2P+/S6Y97s89fipQ4B; session=.eJwNjMEOAiEMRP-l5z3QDRjkZ0jBVo2VNdA9Gf_dnibzJm--UGXyekAR0sUb1A_PNw0eBsXm6aSvKdWOFw8oEK-8hyghxYy99RZiIpRLRsp9R0-Jgqll2OBG97qM7FxVnmo8XSdVX_TopOzVL39_4NUpnA.YhSU8g.tFj0xvOCbYQqgKadxDZxVHM2KO0'
        }
        while url:
            time.sleep(30)
            try:
                response = requests.request("GET", url, headers=headers, data=payload, timeout=100)
                print(response.status_code)
                print(type(response.status_code))
            except Exception as e:
                print(e)
            if response.status_code == 200:
                status = 200
                break

        return status

    def put_notification(self):
        # 创建 target group
        # 192.168.16.119
        logger = PhLogging().phLogger("put_notification", LOG_DEBUG_LEVEL)
        logger.debug("notification 创建流程")
        data = {
            "table_name": "notification"
        }
        item = {}
        status = "resource create success"
        message = {
            "type": "notification",
            "opname": self.project_message.get("owner"),
            "cnotification": {
                "status": status,
                "error": json.dumps({
                    "code": "123",
                    "message": {
                        "zh": status,
                        "en": status
                    }
                }, ensure_ascii=False)
            }
        }

        item.update({"id": self.action_id})
        item.update({"projectId": self.project_id})
        item.update({"category": ""})
        item.update({"code": "0"})
        item.update({"comments": ""})
        item.update({"date": str(int(round(time.time() * 1000)))})
        item.update({"jobCat": "notification"})
        item.update({"jobDesc": self.operate_type})
        item.update({"message": json.dumps(message, ensure_ascii=False)})
        item.update({"owner": self.project_message.get("owner")})
        item.update({"showName": self.project_message.get("showName")})
        item.update({"status": "succeed"})
        data.update({"item": item})
        print(data)
        self.dynamodb.putData(data)
        logger.debug("notification 创建完成")

    def update_ssm(self):
        res = self.ssm.get_ssm_parameter("resource_status")
        project_args = {
            "projectName": self.target_name,
            "status": "default_status",
            "actionId": self.action_id,
            "projectId": self.project_message.get("projectId")
        }
        # 取出list中元素 在进行append
        for resource in res:
            if resource.get("projectId") == self.project_id:
                args_index = res.index(resource)
                project_args = res[args_index]
                res.pop(args_index)
        project_args.update({"status": "started"})
        res.append(project_args)
        self.ssm.put_ssm_parameter("resource_status", json.dumps(res))

    def execute(self):
        self.update_ssm()
        self.put_notification()
