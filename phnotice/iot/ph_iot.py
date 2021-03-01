import abc


class PhIOT(metaclass=abc.ABCMeta):
    client_id = ""

    @abc.abstractmethod
    def build(self):
        """Builder"""
        pass

    @abc.abstractmethod
    def open(self):
        """Open client"""
        pass

    @abc.abstractmethod
    def close(self):
        """Close client"""
        pass

    @abc.abstractmethod
    def publish(self, topic, message):
        """Iot Publish Message"""
        pass