
import subprocess
import os


class DeleteEfs(object):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.efs_path = "/mnt/tmp/"

    def delete_dir(self):

        project_path = self.efs_path + self.project_name + "/"
        if os.path.exists(project_path):

            subprocess.call(["rm", "-rf", project_path])

    def execute(self):
        # 192.168.16.119
        self.delete_dir()

