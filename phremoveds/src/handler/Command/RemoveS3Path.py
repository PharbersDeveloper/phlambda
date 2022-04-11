from handler.Command.Command import Command
from util.AWS.ph_s3 import PhS3


class RemoveS3Path(Command):

    def execute(self, data):
        bucket_name = data["bucket_name"]
        s3_dir = data["s3_dir"]
        PhS3().delete_dir(bucket_name, s3_dir)
