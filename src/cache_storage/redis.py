from hashlib import md5
from typing import Any, Optional
from src.cache_storage import CacheItem, CacheStorage, CacheStorageType
from src.scrapper import ScrapperItem
from redis.asyncio.client import Pipeline
import dill


class RedisCacheStorage(CacheStorage):
    def __init__(self, client: Pipeline):
        super().__init__(CacheStorageType.REDIS)
        self.__client = client

    def hash(self, key: str) -> str:
        return md5(key.encode()).hexdigest()

    async def save(self, item: CacheItem, timeout: Optional[int]):
        """
        Save a single item to Redis cache
        """
        await self.__client.set(self.hash(item.key), dill.dumps(item.data), ex=timeout)
        await self.__client.execute()

    async def save_all(self, data: list[CacheItem], timeout: Optional[int]):
        """
        Save multiple items to Redis cache
        """
        for item in data:
            self.__client.set(self.hash(item.key), dill.dumps(item.data), ex=timeout)
        await self.__client.execute()

    async def get(self, _id: str) -> CacheItem | None:
        """
        Get an item from Redis cache by ID
        """
        _id = self.hash(_id)
        result = await self.__client.get(_id)
        if result:
            return dill.loads(result)
        return None

    async def delete(self, _id: str) -> CacheItem | None:
        """
        Delete an item from Redis cache by ID
        """
        _id = self.hash(_id)
        item = await self.get(_id)
        if item:
            await self.__client.delete(_id)
            await self.__client.execute()
        return item

    async def get_all(self, _ids: list[str]) -> dict[str, Any]:
        """
        Get multiple items from Redis cache by their IDs
        """
        for _id in _ids:
            self.__client.get(self.hash(_id))
        results = await self.__client.execute()
        items = {}
        for index, result in enumerate(results):
            if result is not None:
                item = dill.loads(result)
                items[_ids[index]] = item
        return items
