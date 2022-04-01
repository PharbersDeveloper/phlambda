from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def do_exec(self, data):
        pass
