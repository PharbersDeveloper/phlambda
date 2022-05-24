import gzip
from io import BytesIO
from Logs import Logs
from constants.Errors import FileNotFound, FileCodeError, YarnFilePathError


class Lambda_Logs(Logs):

    def run(self, uri, **kwargs):
        return ""
