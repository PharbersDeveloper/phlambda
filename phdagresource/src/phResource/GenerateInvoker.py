import re

from phResource.commandCreateTargetGroup import CommandCreateTargetGroup
from phResource.commandRegisterTarget import CommandRegisterTarget
from phResource.commandCreateRule import CommandCreateRule
from phResource.commandCreateProject import CommandCreateProject
from phResource.commandCreateEfs import CommandCreateEfs


class GenerateInvoker:

    commands = {
        "CommandCreateTargetGroup": CommandCreateTargetGroup()
    }

    def name_convert_to_camel(self, name):

        return re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), name.lower())

    def execute(self):

        project_name = "Auto_Raw_Data"
        target_name = self.name_convert_to_camel(project_name)
        target_ip = "192.168.16.119"
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


        pass

