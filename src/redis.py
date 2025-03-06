import contextlib
from typing import Any, AsyncIterator
from redis.asyncio.client import Pipeline

import redis.asyncio as redis
from redis.asyncio import connection


class RedisCacheManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None) -> None:
        if engine_kwargs is None:
            engine_kwargs = {}
        self._pool: connection.ConnectionPool | None = redis.ConnectionPool.from_url(
            host, **engine_kwargs
        )

    async def close(self):
        if self._pool is None:
            raise Exception("CacheManager is not initialized")
        await self._pool.aclose()
        self._pool = None

    @property
    def is_closed(self) -> bool:
        return self._pool is None

    @contextlib.asynccontextmanager
    async def connection(self) -> AsyncIterator[redis.Redis]:
        if self._pool is None:
            raise Exception("CacheManager is not initialized")
        client = redis.Redis(connection_pool=self._pool, protocol=3)
        try:
            yield client
        finally:
            await client.aclose()

    @contextlib.asynccontextmanager
    async def pipeline(self) -> AsyncIterator[Pipeline]:
        if self._pool is None:
            raise Exception("CacheManager is not initialized")
        if self._pool.can_get_connection():
            client = redis.Redis(connection_pool=self._pool, protocol=3)
            try:
                async with client.pipeline(transaction=True) as pipe:
                    yield pipe
            finally:
                await client.aclose()
        else:
            raise Exception(
                f"Cache connection limit exceeded. Max connections = {self._pool.max_connections}"
            )


manager = RedisCacheManager("redis://localhost:6379/0")


async def get_cache() -> AsyncIterator[Pipeline]:
    async with manager.pipeline() as pipeline:
        yield pipeline


__all__ = ["get_cache"]
