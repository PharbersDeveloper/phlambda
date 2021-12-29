from redis import ConnectionPool, Redis


class SingletonMetaClass(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class PhRedis(metaclass=SingletonMetaClass):

    def __init__(self, **kwargs):
        pool = ConnectionPool(**kwargs, max_connections=10, decode_responses=True)
        self.redis = Redis(connection_pool=pool)

    def getRedis(self):
        return self.redis


