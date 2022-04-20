
import gzip
from io import BytesIO
from Logs import Logs
from constants.Errors import FileNotFound


class Step_Logs(Logs):

    def read_gz(self, gz_data):
        gzipfile = BytesIO(gz_data)
        return gzip.GzipFile(fileobj=gzipfile).read()


    def run(self, uri, **kwargs):
        bucket = uri.split('/')[0]
        uri = uri[len(bucket)+1:]

        result = self.get_data(bucket, uri)
        if not result:
            raise FileNotFound("logs file not exit")

        log_file = self.read_gz(result).decode()
        return log_file
