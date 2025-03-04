from typing import NamedTuple
from src.object_storage import ObjectStorage, ObjectStorageType
from src.scrapper import ScrapperItem
import os


class ObjectInfo(NamedTuple):
    name: str
    url: str


class LocalObjectStorage(ObjectStorage[ObjectInfo]):
    def __init__(self, root_dir: str):
        super().__init__(ObjectStorageType.LOCAL)
        self.__root_dir = root_dir

    async def save(self, data: ObjectInfo) -> str:
        downloaded_data = await self._download(data.url)
        location = f"{self.__root_dir}/{data.name}.jpg"
        os.makedirs(os.path.dirname(location), exist_ok=True)
        with open(location, "wb") as f:
            f.write(downloaded_data)
            location = f.name
        return location

    async def save_all(self, data: list[ObjectInfo]) -> dict[str, str]:
        results = {}
        for obj in data:
            location = await self.save(obj)
            results[obj.name] = location
        return results

    async def get(self, _id: str) -> str | None:
        location = f"{self.__root_dir}/{_id}.jpg"
        if os.path.exists(location):
            return location
        return None

    async def delete(self, _id: str) -> str | None:
        location = f"{self.__root_dir}/{_id}.jpg"
        if os.path.exists(location):
            os.remove(location)
            return location
        return None
