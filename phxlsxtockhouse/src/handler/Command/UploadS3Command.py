
from handler.Command.Command import Command
from util.AWS.ph_s3 import PhS3


class UploadS3Command(Command):

    def execute(self, data):
        source = data["source"]
        bucket_name = data["bucket_name"]
        s3_dir = data["s3_dir"]
        s3 = PhS3()
        s3.upload_dir(source, bucket_name, s3_dir)
