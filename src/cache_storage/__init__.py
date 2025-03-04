from abc import abstractmethod
import enum
from re import I
from typing import Any, NamedTuple, Optional


class CacheStorageType(enum.StrEnum):
    IN_MEMORY = "in_memory"
    REDIS = "redis"


class CacheItem(NamedTuple):
    data: Any
    key: str


class CacheStorage:
    def __init__(self, storage_type: CacheStorageType):
        self.__storage_type = storage_type

    @property
    def storage_type(self):
        return self.__storage_type

    @abstractmethod
    async def save(self, item: CacheItem, timeout: Optional[int]):
        pass

    @abstractmethod
    async def save_all(self, data: list[CacheItem], timeout: Optional[int]):
        pass

    @abstractmethod
    async def get(self, _id: str) -> Any | None:
        pass

    @abstractmethod
    async def delete(self, _id: str) -> Any | None:
        pass

    @abstractmethod
    async def get_all(self, _ids: list[str]) -> dict[str, Any]:
        pass
