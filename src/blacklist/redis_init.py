from collections.abc import Iterator

import redis

from config import settings


def init_redis_pool() -> Iterator[redis.Redis]:
    session = redis.Redis(host=settings.REDIS_HOSTNAME, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD, decode_responses=True)
    yield session
    session.close()


