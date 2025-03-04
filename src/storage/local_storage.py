import json

from src.scrapper import ScrapperItem
from src.storage import Storage, StorageType
import os


class LocalStorage(Storage[ScrapperItem]):
    def __init__(self, path: str):
        super().__init__(StorageType.LOCAL)
        self.__path = path

    async def save(self, data: ScrapperItem):
        file_content = await self.load()
        file_content.append(data)
        new_file_content = json.dumps(file_content, indent=4, sort_keys=True)
        with open(self.__path, "w") as f:
            f.write(new_file_content)

    async def upsert(self, data: ScrapperItem):
        file_content = await self.load()
        file_content = [
            item for item in file_content if item["product_title"] != data["product_title"]
        ]
        file_content.append(data)
        new_file_content = json.dumps(file_content, indent=4, sort_keys=True)
        with open(self.__path, "w") as f:
            f.write(new_file_content)

    async def save_all(self, data: list[ScrapperItem]):
        file_content = await self.load()
        titles = set(item["product_title"] for item in data)
        file_content = [item for item in file_content if item["product_title"] not in titles]
        file_content.extend(data)
        new_file_content = json.dumps(file_content, indent=4, sort_keys=True)
        with open(self.__path, "w") as f:
            f.write(new_file_content)

    async def upsert_all(self, data: list[ScrapperItem]):
        file_content = await self.load()
        titles = set(item["product_title"] for item in data)
        file_content = [item for item in file_content if item["product_title"] not in titles]
        file_content.extend(data)
        new_file_content = json.dumps(file_content, indent=4, sort_keys=True)
        with open(self.__path, "w") as f:
            f.write(new_file_content)

    async def get(self, _id: str) -> ScrapperItem | None:
        file_content = await self.load()
        for item in file_content:
            if item["product_title"] == _id:
                return item
        return None

    async def delete(self, _id: str) -> ScrapperItem | None:
        file_content = await self.load()
        for item in file_content:
            if item["product_title"] == _id:
                file_content.remove(item)
                new_file_content = json.dumps(file_content, indent=4, sort_keys=True)
                with open(self.__path, "w") as f:
                    f.write(new_file_content)
                return item

    async def load(self) -> list[ScrapperItem]:
        if not os.path.exists(self.__path):
            os.makedirs(os.path.dirname(self.__path), exist_ok=True)
            with open(self.__path, "w") as f:
                f.write("")
            return []

        with open(self.__path, "r") as f:
            file_content = f.read()
            return json.loads(file_content) if file_content else []
