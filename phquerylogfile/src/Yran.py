
import gzip
import boto3
from io import BytesIO
from Logs import Logs
from constants.Errors import FileNotFound


class Yran_Logs(Logs):

    def __init__(self):
        self.s3 = boto3.client('s3')


    def if_exit(self, bucket, key):
        try:
            response = self.s3.get_object(Bucket=bucket, Key=key)
            return response.get('Body').read()
        except:
            return


    def read_file(self, bucket, key):
        path = key.split('/')[-1]
        self.s3.download_file(Filename=f"/tmp/{path}", Bucket=bucket, Key=key)
        filehandler = open("/tmp/"+path, "rb")
        filelines = filehandler.readlines()
        data = ''
        for i in filelines:
            data += i.decode("utf-8", "ignore")
        return data


    def read_gz(self, gz_data):
        gzipfile = BytesIO(gz_data)
        return gzip.GzipFile(fileobj=gzipfile).read()


    def query_logfile(self, bucket, file_key):
        response = self.s3.list_objects_v2(
            Bucket=f'{bucket}',
            Prefix=f'2020-11-11/emr/yarnLogs/hadoop/logs-tfile/{file_key}/',
            MaxKeys=100)
        return [i.get('Key') for i in response.get('Contents', {})]


    def run(self, uri, bucket="ph-platform", **kwargs):
        result = self.if_exit(bucket, uri + "stderr.gz")
        if not result:
            raise FileNotFound("logs file not exit")

        log_file = self.read_gz(result).decode()
        file_name = log_file[log_file.rfind('application_'): log_file.rfind('application_') + 30]
        logkey_list = self.query_logfile(bucket, file_name)

        data = ""
        for i in logkey_list:
            data += self.read_file(bucket, i)
        if not data:
            raise FileNotFound("logs file not exit")
        return data
