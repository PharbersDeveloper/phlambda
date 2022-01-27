
from phResource.command import Command
from util.AWS.ELB import ELB
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class CommandDelTargetGroup(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.elb = ELB()

    def execute(self):
        # 创建 target group
        # 192.168.16.119
        logger = PhLogging().phLogger("del_target_group", LOG_DEBUG_LEVEL)
        logger.debug("target_group 删除流程")
        project_args = self.ssm.get_ssm_parameter(self.target_name + "-project")
        target_group_arn = project_args.get("target_group_arn")
        self.elb.delete_target_group(target_group_arn=target_group_arn)

        logger.debug("target_group 删除完成")
        return target_group_arn
