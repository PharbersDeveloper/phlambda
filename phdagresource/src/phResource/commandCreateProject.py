import json
import os
from phResource.command import Command
from util.AWS.CFN import CFN
from util.AWS.ELB import ELB
from util.AWS.EC2 import EC2
from util.AWS.SSM import SSM
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class CommandCreateProject(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.cfn = CFN()
        self.elb = ELB()
        self.ec2 = EC2()
        self.ssm = SSM()

    def get_cluster_id(self):

        cluster_id = self.ssm.get_str_ssm_parameter("cluster_id")
        return cluster_id

    def create_parameter(self):
        parameter = {
            "projectName": self.target_name,
            "currentContext": os.getenv("EDITION"),
            "proxies": [
                self.target_ip
            ],
            "dns": f"https://{self.project_id}.pharbers.com/",
            "clusters": [
                {
                    "type": "emr",
                    "id": self.get_cluster_id()
                }
            ],
            "olap": [
                {
                    "type": "ch",
                    "name": "proxy",
                    "uri": f"http://{self.target_ip}:8123"
                },
                {
                    "type": "ch",
                    "name": "http",
                    "uri": f"http://{self.target_ip}:8080/ch?"
                }
            ],
            "notification": self.action_id,
            "commargs": [
                {
                    "engine": "pyspark",
                    "type": "spark-submit",
                    "args": {
                        'spark.driver.cores': '1',
                        'spark.driver.memory': '2g',
                        'spark.executor.cores': '2',
                        'spark.executor.memory': '4g',
                        'spark.executor.instances': '2',
                        'spark.driver.extraJavaOptions': '-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8 -Dcom.amazonaws.services.s3.enableV4',
                        'spark.executor.extraJavaOptions': '-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8 -Dcom.amazonaws.services.s3.enableV4'
                    }
                }
            ]
        }

        return json.dumps(parameter)

    def execute(self):
        # 192.168.16.119
        logger = PhLogging().phLogger("creat_ec2", LOG_DEBUG_LEVEL)
        logger.debug(self.target_name)
        logger.debug(self.target_ip)
        Priority = self.elb.get_rules_len()
        # 获取当前project 的 volume id
        volumeId = self.ec2.get_volume_id(self.project_id)
        # 创建当前project的 parameter
        parameter = self.create_parameter()
        logger.debug("print ssm parameter")
        logger.debug(parameter)
        self.cfn.create_project(self.target_name, self.target_ip, self.project_id, str(Priority), volumeId, parameter)
