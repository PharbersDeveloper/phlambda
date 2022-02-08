import re
import random
import json

from util.AWS.SSM import SSM

from phResource.commandCreateTargetGroup import CommandCreateTargetGroup
from phResource.commandRegisterTarget import CommandRegisterTarget
from phResource.commandCreateRule import CommandCreateRule
from phResource.commandCreateProject import CommandCreateProject
from phResource.commandCreateEfs import CommandCreateEfs
from phResource.commandDeleteEfs import CommandDelEfs
from phResource.commandPutParameter import CommandPutParameter
from phResource.commandCreateRecords import CommandCreateRecords
from phResource.commandDelParameter import CommandDelParameter
from phResource.commandDelProject import CommandDelProject
from phResource.commandDelRule import CommandDelRule
from phResource.commandDelTargetGroup import CommandDelTargetGroup
from phResource.commandDelRecords import CommandDelRecords
from phResource.commandPutResouceArgs import CommandPutResourceArgs
from phResource.commandDelResouceArgs import CommandDelResourceArgs
from phResource.commandGetResouceArgs import CommandGetResourceArgs

from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class GenerateInvoker(object):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
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

        project_name = self.project_name
        project_id = self.project_id
        
        target_name = self.name_convert_to_camel(project_name)
        # 分配Ip 并从SSM判断ip是否重复
        target_ip = self.create_ip_address()
        logger.debug(target_name)
        logger.debug(target_ip)

        try:
            # 创建records
            CommandCreateRecords(target_name=target_name).execute()
        except Exception as e:
            status = "创建records时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)
        
        try:
            # 创建target group
            target_group_arn = CommandCreateTargetGroup(target_name=target_name).execute()
        except Exception as e:
            status = "创建 target group 时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            # register targets
            CommandRegisterTarget(target_ip=target_ip, target_group_arn=target_group_arn).execute()
        except Exception as e:
            status = "register targets 时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            # 向load balancer 添加rules
            rule_arn = CommandCreateRule(target_name=target_name, target_group_arn=target_group_arn).execute()
        except Exception as e:
            status = "向load balancer 添加rules 时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            # 在efs里创建相关文件夹
            # 不能直接创建efs 需要sns调用另一个lambda创建删除efs
            CommandCreateEfs(target_name=target_name).execute()
        except Exception as e:
            status = "在efs里创建相关文件夹时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            # 创建ec2实例
            CommandCreateProject(target_name=target_name, target_ip=target_ip).execute()
        except Exception as e:
            status = "创建ec2实例 时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            # 更新ssm
            CommandPutParameter(
                target_name=target_name,
                target_ip=target_ip
            ).execute()
        except Exception as e:
            status = "更新ssm 时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            # 在dynamodb更新 resource 相关的参数
            CommandPutResourceArgs(
                target_name=target_name,
                project_id=project_id,
                target_ip=target_ip,
                target_group_arn=target_group_arn,
                rule_arn=rule_arn
            ).execute()
        except Exception as e:
            status = "创建ResourceArgs 时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)




    def delete_execute(self):
        logger = PhLogging().phLogger("delete_project", LOG_DEBUG_LEVEL)
        logger.debug("project删除流程")

        project_name = self.project_name
        project_id = self.project_id
        target_name = self.name_convert_to_camel(project_name)
        logger.debug(target_name)

        try:
            # 删除ec2 实例
            CommandDelProject(target_name=target_name).execute()
        except Exception as e:
            status = "删除ec2 实例错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            # 从dynamodb中获取 project 的相关参数
            resource_args = CommandGetResourceArgs(target_name=target_name, project_id=project_id).execute()
        except Exception as e:
            status = "从dynamodb获取project参数错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            # 删除efs 相关文件
            # 不能直接创建efs 需要sns调用另一个lambda创建删除efs
            CommandDelEfs(target_name=target_name).execute()
        except Exception as e:
            status = "在efs里创建相关文件夹时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            # 删除 load balancer 里的 rule
            CommandDelRule(target_name=target_name, resource_args=resource_args).execute()
        except Exception as e:
            status = "删除 load balancer 里的 rule 时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            # 删除 target group
            CommandDelTargetGroup(target_name=target_name, resource_args=resource_args).execute()
        except Exception as e:
            status = "删除 target时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            # 删除 records
            CommandDelRecords(target_name=target_name).execute()
        except Exception as e:
            status = "删除 records 时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            # 删除ssm 中当前project资源
            CommandDelParameter(target_name=target_name).execute()
        except Exception as e:
            status = "删除ssm 中当前project资源 时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)

        try:
            # 删除resource args
            CommandDelResourceArgs(target_name=target_name, project_id=project_id).execute()
        except Exception as e:
            status = "删除dynamodb args 时错误:" + json.dumps(str(e), ensure_ascii=False)
            logger.debug(status)




    def execute(self):
        logger = PhLogging().phLogger("选择对project的操作", LOG_DEBUG_LEVEL)
        logger.debug(self.project_type)
        logger.debug(self.project_name)
        logger.debug(self.project_id)
        if self.project_type == "project_create":
            self.create_execute()
        elif self.project_type == "project_delete":
            self.delete_execute()



if __name__ == '__main__':

    app = GenerateInvoker()
    app.execute()