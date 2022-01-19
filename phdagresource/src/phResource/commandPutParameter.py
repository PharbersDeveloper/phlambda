import subprocess
import json

from phResource.command import Command
from util.AWS.SSM import SSM

class CommandPutParameter(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.ssm = SSM()

    def update_parameter(self):

        # 先获取相关parameter
        param_list = ["project_diver_args", "project_args", "userIp"]

        # 先获取userIp 进行增加
        userIp_value = self.ssm.get_ssm_parameter("usersIp")
        userIp_value.update({self.target_name: self.target_ip})
        self.ssm.put_ssm_parameter("userIp", json.dumps(userIp_value))

        # 获取 project_args
        project_args_value = self.ssm.get_ssm_parameter("projects_args")
        project_args_value.update({self.target_name: "http://" + self.target_ip + ":8080/ch?"})
        self.ssm.put_ssm_parameter("projects_args", json.dumps(project_args_value))

        # 更新 project_diver_args
        project_diver_args = self.ssm.get_ssm_parameter("project_dirver_args")
        project_diver_args.update({self.target_name: "http://" + self.target_ip + ":8123"})
        self.ssm.put_ssm_parameter("project_diver_args", json.dumps(project_diver_args))


    def execute(self):
        # 192.168.16.119

        self.update_parameter()

        pass
