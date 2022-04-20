import gzip
from io import BytesIO
from Logs import Logs
from constants.Errors import FileNotFound, FileCodeError


class Yarn_Logs(Logs):

    def read_file(self, bucket, key):
        data = self.get_data(bucket, key)
        try:
            data = data.decode("utf-8", "ignore")
            return data
        except:
            raise FileCodeError("file decode error")


    def read_gz(self, gz_data):
        gzipfile = BytesIO(gz_data)
        return gzip.GzipFile(fileobj=gzipfile).read()


    def query_logfile(self, bucket, file_key):
        response = self.s3.list_objects_v2(
            Bucket=f'{bucket}',
            Prefix=file_key,
            MaxKeys=100)
        return [i.get('Key') for i in response.get('Contents', {})]


    def run(self, uri, **kwargs):
        bucket = uri.split('/')[0]
        uri = uri[len(bucket) + 1:]
        logkey_list = self.query_logfile(bucket, uri)

        data = ""
        for i in logkey_list:
            data += self.read_file(bucket, i)
        if not data:
            raise FileNotFound("logs file not exit")
        return data
