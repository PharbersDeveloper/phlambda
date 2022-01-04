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

    # 以下并未做任何抽象
    def get_count(self, sql):
        return list(self.__client.execute(sql).pop()).pop()

    def exec_ddl_sql(self, sql):
        return self.__client.execute(sql)

    def insert_data(self, sql, values):
        return self.__client.execute(sql, values)
