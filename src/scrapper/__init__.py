from typing import Optional, TypedDict


class ScrapperItem(TypedDict):
    product_title: str
    product_price: Optional[str]
    path_to_image: Optional[str]


__all__ = ["ScrapperItem"]
