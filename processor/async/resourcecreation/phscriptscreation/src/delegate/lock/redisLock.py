
import os
from redis import Redis, ConnectionPool

redis_connect = {
    'host': os.environ.get('REDIS_HOST'),
    'port': os.environ.get('REDIS_PORT')
}


def create_redis_lock():
    pool = ConnectionPool(**redis_connect, max_connections=10, decode_responses=True)
    rediscli:Redis = Redis(connection_pool=pool)

    return rediscli