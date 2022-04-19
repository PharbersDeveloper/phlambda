from abc import ABC, abstractmethod


class Logs(ABC):

    @abstractmethod
    def run(self, **kwargs):
        pass
