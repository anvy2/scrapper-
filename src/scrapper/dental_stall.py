from typing import Optional

import bs4
from fastapi import HTTPException, status
import httpx


from src.cache_storage import CacheItem, CacheStorage
from src.decorators.retry import retry_async
from src.notification import Notification
from src.object_storage import ObjectStorage
from src.object_storage.local import ObjectInfo
from src.scrapper import ScrapperItem
from src.storage import Storage
from src.utils import format_proxy


class Scrapper:
    def __init__(
        self,
        storage: Storage,
        cache: CacheStorage,
        notification: Notification,
        object_storage: ObjectStorage[ObjectInfo],
        proxy: Optional[str] = None,
    ):
        self.__url = "https://dentalstall.com/shop"
        self.__storage = storage
        self.__cache = cache
        self.__notification = notification
        self.__object_storage = object_storage
        self.__client = self._setup_client(proxy)

    def _setup_client(self, proxy: Optional[str] = None) -> httpx.AsyncClient:
        client_kwargs = {}
        if proxy:
            client_kwargs["proxy"] = format_proxy(proxy)
        return httpx.AsyncClient(**client_kwargs)

    @retry_async(max_tries=1, delay=1)
    async def scrap(self, user_id: str, page_limit: Optional[int] = None):
        response = await self.__client.get(self.__url)
        if (response.status_code // 100) != 2:
            return HTTPException(status_code=response.status_code, detail=response.text)
        data = response.text
        soup = bs4.BeautifulSoup(data, "lxml")
        page_numbers = soup.find(name="ul", class_="page-numbers")
        if not page_numbers:
            return
        total_pages = 1
        pages = page_numbers.find_all(name="a")  # type: ignore
        if "next" in pages[-1].text.lower():
            total_pages = int(pages[-2].text)
        if page_limit is None:
            page_limit = total_pages
        total_items = []
        for page in range(1, min(page_limit, total_pages) + 1):
            items = await self._scrap_page(page)
            total_items.extend(items)
        titles = set(item["product_title"] for item in total_items)
        images = set(
            item["path_to_image"] for item in total_items if item["path_to_image"] is not None
        )
        total_items_count = len(total_items)
        cached_data: dict[str, ScrapperItem] = await self.__cache.get_all(list(titles))
        cached_images: dict[str, str] = await self.__cache.get_all(list(images))
        images_to_save: list[ScrapperItem] = []
        items_to_save: list[ScrapperItem] = []
        new_cache_data: list[CacheItem] = []
        new_cache_image_data: list[CacheItem] = []
        for item in total_items:
            if item["path_to_image"] is not None:
                if item["path_to_image"] not in cached_images:
                    image = await self.__object_storage.save(
                        ObjectInfo(name=item["product_title"], url=item["path_to_image"])
                    )
                    new_cache_image_data.append(CacheItem(key=item["path_to_image"], data=image))
                    item["path_to_image"] = image
                    images_to_save.append(item)
                else:
                    item["path_to_image"] = cached_images[item["path_to_image"]]

            if (
                item["product_title"] not in cached_data
                or item["product_price"] != cached_data[item["product_title"]]["product_price"]
            ):
                items_to_save.append(item)
                new_cache_data.append(CacheItem(key=item["product_title"], data=item))

        if items_to_save:
            await self.__storage.upsert_all(items_to_save)
            await self.__cache.save_all(new_cache_data, None)
        if new_cache_image_data:
            await self.__cache.save_all(new_cache_image_data, None)
        await self.__notification.notify(
            user_id=user_id, message=f"Scrapped {total_items_count} items"
        )

    @retry_async(max_tries=1, delay=1)
    async def _scrap_page(self, page: int) -> list[ScrapperItem]:
        url = f"{self.__url}/page/{page}"
        response = await self.__client.get(url)
        if response.status_code == status.HTTP_301_MOVED_PERMANENTLY:
            url = str(response.next_request.url)  # type: ignore
            response = await self.__client.get(url)
        if (response.status_code // 100) != 2:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = []
        soup = bs4.BeautifulSoup(response.text, "lxml")
        products = soup.find_all(name="div", class_="product-inner")
        for product in products:  # type: ignore
            thumbnail: Optional[str] = None
            thumbnail_tag = product.find(  # type: ignore
                name="img",  # type: ignore
                class_="attachment-woocommerce_thumbnail size-woocommerce_thumbnail",
            )
            if thumbnail_tag is not None:
                thumbnail = thumbnail_tag.attrs["data-lazy-src"]  # type: ignore
            title = product.find(name="h2", class_="woo-loop-product__title").getText()  # type: ignore
            price = product.find(name="span", class_="price")  # type: ignore
            if price is not None and price.find("del") is not None:  # type: ignore
                price = price.find("ins")  # type: ignore
            price_text = (
                (
                    price.getText()  # type: ignore
                    .replace(
                        price.find("span", class_="woocommerce-Price-currencySymbol").getText(),  # type: ignore
                        "",
                    )
                    .strip()
                )
                if price is not None
                else None
            )
            item = ScrapperItem(
                product_title=title,
                product_price=price_text,
                path_to_image=thumbnail,
            )
            data.append(item)
        return data


__all__ = ["Scrapper"]
