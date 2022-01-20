import subprocess
import os

from phResource.command import Command


class CommandCreateEfs(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.efs_path = "/mnt/tmp/"

    def create_dir(self):

        project_path = self.efs_path + self.target_name + "/"
        if not os.path.exists(project_path):
            dir_list = ["airflow", "chdumps", "tmp", "workspace"]
            for dir in dir_list:
                subprocess.call(["mkdir", "-p", project_path + dir])
            # 复制airflow 文件
            # 复制/mnt/tmp/airflow 文件夹到 project_path + airflow
            subprocess.call(["cp", "-r", self.efs_path + "airflow/", project_path])

            # 复制 chdumps 文件
            # 复制 /mnt/tmp/chdumps 文件夹到 project_path + chdumps
            subprocess.call(["cp", "-r", self.efs_path + "airflow/", project_path])


    def execute(self):
        # 192.168.16.119

        self.create_dir()

        pass
