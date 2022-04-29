import subprocess
import os
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
        param_list = ["project_driver_args", "project_args", "userIp", "airflow_args"]

        # 先获取userIp 进行增加
        userIp_value = self.ssm.get_ssm_parameter("usersIp")
        userIp_value.update({self.target_name: self.target_ip})
        self.ssm.put_ssm_parameter("usersIp", json.dumps(userIp_value))

    def execute(self):
        # 192.168.16.119

        self.update_parameter()
        parameter = self.create_parameter()

        return parameter
