import subprocess

from phResource.command import Command


class CommandCreateEfs(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.efs_path = "/mnt/tmp/"

    def create_dir(self):

        project_path = self.efs_path + self.target_name + "/"
        dir_list = ["airflow", "chdumps", "tmp", "workspace"]
        for dir in dir_list:
            subprocess.call(["mkdir", "-p", project_path + dir])
        # 复制airflow 文件
        # 复制chdumps 文件

        # dump_path = project_path + "chdumps"
        # workspace_path = project_path + "workspace"
        # tmp_path = project_path + "tmp"
        # airflow = project_path + "airflow"


    def execute(self):
        # 192.168.16.119

        self.create_dir()

        pass
