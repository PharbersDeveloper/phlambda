import re
import random

from util.AWS.SSM import SSM

from phResource.commandCreateTargetGroup import CommandCreateTargetGroup
from phResource.commandRegisterTarget import CommandRegisterTarget
from phResource.commandCreateRule import CommandCreateRule
from phResource.commandCreateProject import CommandCreateProject
from phResource.commandCreateEfs import CommandCreateEfs
from phResource.commandPutParameter import CommandPutParameter
from phResource.commandCreateRecords import CommandCreateRecords

from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class GenerateInvoker:

    commands = {
        "CommandCreateTargetGroup": CommandCreateTargetGroup()
    }
    def __init__(self):
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


    def execute(self):
        logger = PhLogging().phLogger("creat_project", LOG_DEBUG_LEVEL)
        logger.debug("project创建流程")

        project_name = "Auto_Raw_Data"
        target_name = self.name_convert_to_camel(project_name)
        # 分配Ip 并从SSM判断ip是否重复
        target_ip = self.create_ip_address()
        logger.debug(target_name)


        # 创建records
        CommandCreateRecords(target_name=target_name).execute()

        # 创建target group
        target_group_arn = CommandCreateTargetGroup(target_name=target_name).execute()

        # register targets
        CommandRegisterTarget(target_ip=target_ip, target_group_arn=target_group_arn).execute()

        # 向load balancer 添加rules
        CommandCreateRule(target_name=target_name, target_group_arn=target_group_arn).execute()

        # 在efs里创建相关文件夹
        CommandCreateEfs(target_name=target_name).execute()

        # 创建ec2实例
        CommandCreateProject(target_name=target_name).execute()

        # 更新ssm
        CommandPutParameter(target_name=target_name, target_ip=target_ip).execute()


if __name__ == '__main__':

    app = GenerateInvoker()
    app.execute()