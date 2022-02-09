from abc import ABC, abstractmethod
from util.AWS.ph_s3 import PhS3


class Strategy(ABC):

    def __init__(self):
        self.phs3 = PhS3()

    @abstractmethod
    def do_execution(self, data):
        pass

    def load(self, path):
        with open(path, "r") as file:
            return file.read()
