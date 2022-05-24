
import gzip
from io import BytesIO
from Logs import Logs
from constants.Errors import FileNotFound, StepFilePathError


class Emr_Logs(Logs):

    def run(self, uri, **kwargs):
        return ""
