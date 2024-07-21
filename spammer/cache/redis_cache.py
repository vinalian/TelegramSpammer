from redis import Redis, ConnectionPool
from os import environ


__all__ = [
    'redis'
]

REDIS_POOL = ConnectionPool(
    host=environ.get('REDIS_HOST'),
    port=environ.get('REDIS_PORT'),
    db=1,
    max_connections=10,
)

redis = Redis(connection_pool=REDIS_POOL)
