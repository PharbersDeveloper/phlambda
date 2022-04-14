from util.ClieckHouse import SingletonMetaClass
from redis import ConnectionPool, Redis


class PhRedis(object):

    def __init__(self, **kwargs):
        pool = ConnectionPool(**kwargs, max_connections=10, decode_responses=True)
        self.redis = Redis(connection_pool=pool)

    def getRedis(self):
        return self.redis


