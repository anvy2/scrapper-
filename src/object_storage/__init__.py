from abc import abstractmethod
import enum
from typing import Optional

import httpx


class ObjectStorageType(enum.StrEnum):
    LOCAL = "local"
    S3 = "s3"


class ObjectStorage[T]:
    def __init__(self, storage_type: ObjectStorageType, proxy: Optional[str] = None):
        self.__storage_type = storage_type
        self._client = self._setup_client(proxy)

    @property
    def storage_type(self):
        return self.__storage_type

    def _setup_client(self, proxy: Optional[str] = None) -> httpx.AsyncClient:
        client_kwargs = {}
        if proxy:
            client_kwargs["proxy"] = proxy
        return httpx.AsyncClient(**client_kwargs)

    async def _download(self, url: str) -> bytes:
        response = await self._client.get(url)
        return response.content

    @abstractmethod
    async def save(self, data: T) -> str:
        pass

    @abstractmethod
    async def save_all(self, data: list[T]) -> dict[str, str]:
        pass

    @abstractmethod
    async def get(self, _id: str) -> str | None:
        pass

    @abstractmethod
    async def delete(self, _id: str) -> str | None:
        pass
