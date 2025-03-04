from abc import abstractmethod
import enum


class StorageType(enum.StrEnum):
    LOCAL = "local"
    S3 = "s3"
    MYSQL = "mysql"
    POSTGRES = "postgres"


class Storage[T]:
    def __init__(self, storage_type: StorageType):
        self.__storage_type = storage_type

    @property
    def storage_type(self):
        return self.__storage_type

    @abstractmethod
    async def save(self, data: T):
        pass

    @abstractmethod
    async def save_all(self, data: list[T]):
        pass

    @abstractmethod
    async def get(self, _id: str) -> T | None:
        pass

    @abstractmethod
    async def delete(self, _id: str) -> T | None:
        pass

    @abstractmethod
    async def upsert(self, data: T):
        pass

    @abstractmethod
    async def upsert_all(self, data: list[T]):
        pass
