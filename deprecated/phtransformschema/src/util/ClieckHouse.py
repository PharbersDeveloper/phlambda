from clickhouse_driver import Client


class SingletonMetaClass(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class ClickHouse(metaclass=SingletonMetaClass):
    def __init__(self, *args, **kwargs):
        self.__client = Client(*args, **kwargs)

    def getClient(self):
        return self.__client
