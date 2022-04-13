import re
import random
import json

from util.AWS.SSM import SSM

from phResource.commandCreateProject import CommandCreateProject
from phResource.commandPutParameter import CommandPutParameter
from phResource.commandDelParameter import CommandDelParameter
from phResource.commandDelProject import CommandDelProject
from phResource.commandPutResouceArgs import CommandPutResourceArgs
from phResource.commandDelResouceArgs import CommandDelResourceArgs
from phResource.commandGetResouceArgs import CommandGetResourceArgs
from phResource.commandPutNotification import CommandPutNotification

from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class GenerateInvoker(object):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.operate_type = self.item.get("jobCat")
        self.project_message = json.loads(self.item.get("message"))
        self.action_id = self.item.get("id")
        self.ssm = SSM()

    def name_convert_to_camel(self, name):
        return re.sub(r'(_[a-z])', lambda x: x.group(1)[1], name.lower())

    def create_ip_address(self):
        ip_address = "192.168.16." + str(random.randint(100, 255))

        parameter_name = "usersIp"
        value = self.ssm.get_ssm_parameter(parameter_name)
        ip_list = list(value.values())
        if ip_address in ip_list:
            ip_address = self.create_ip_address()

        return ip_address

    def create_execute(self):
        logger = PhLogging().phLogger("creat_project", LOG_DEBUG_LEVEL)
        logger.debug("project创建流程")

        project_name = self.project_message.get("projectName")
        project_id = self.project_message.get("projectId")
        content = self.project_message.get("content")

        target_name = self.name_convert_to_camel(project_name)
        # 分配Ip 并从SSM判断ip是否重复
        target_ip = self.create_ip_address()
        logger.debug(target_name)
        logger.debug(target_ip)

        try:
            # 更新ssm
            CommandPutParameter(
                target_name=target_name,
                target_ip=target_ip,
                project_id=project_id
            ).execute()
        except Exception as e:
            status = "更新ssm 时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            # 创建ec2实例
            CommandCreateProject(
                target_name=target_name,
                target_ip=target_ip,
                project_id=project_id,
                project_message=self.project_message,
                action_id=self.action_id).execute()
        except Exception as e:
            status = "创建ec2实例 时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            CommandPutNotification(action_id=self.action_id, operate_type=self.operate_type, project_message=self.project_message).execute()
        except Exception as e:
            status = "put notification  时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

    def delete_execute(self):
        logger = PhLogging().phLogger("delete_project", LOG_DEBUG_LEVEL)
        logger.debug("project删除流程")

        project_name = self.project_message.get("projectName")
        project_id = self.project_message.get("projectId")
        content = self.project_message.get("content")
        target_name = self.name_convert_to_camel(project_name)
        logger.debug(target_name)

        try:
            # 删除ec2 实例
            CommandDelProject(target_name=project_id).execute()
        except Exception as e:
            status = "删除ec2 实例错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

    def execute(self):
        logger = PhLogging().phLogger("选择对project的操作", LOG_DEBUG_LEVEL)

        if self.operate_type == "resource_create":
            self.create_execute()
        elif self.operate_type == "resource_delete":
            self.delete_execute()



if __name__ == '__main__':

    app = GenerateInvoker()
    app.execute()