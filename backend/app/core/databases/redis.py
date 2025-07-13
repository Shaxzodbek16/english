from functools import cache
from typing import AsyncGenerator

import redis.asyncio as redis
from app.core.settings import get_settings

settings = get_settings()


@cache
def get_redis_pool():
    return redis.ConnectionPool.from_url(
        f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
        encoding="utf-8",
        decode_responses=True,
        max_connections=10,
    )


async def get_redis_connection() -> AsyncGenerator[redis.Redis, None]:
    conn = redis.Redis(connection_pool=get_redis_pool())
    try:
        yield conn
    finally:
        await conn.aclose()
