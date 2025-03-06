import http
from typing import Annotated, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response

from src.redis import get_cache
from src.cache_storage.redis import RedisCacheStorage
from src.dependencies import verify_api_key
from src.notification.console import ConsoleNotification
from src.object_storage.local import LocalObjectStorage
from src.scrapper.dental_stall import Scrapper
from src.storage.local_storage import LocalStorage
from src.redis import Pipeline

router = APIRouter(prefix="/scrapper", tags=["scrapper"])


@router.post("/scrap", dependencies=[Depends(verify_api_key)])
async def scrap(
    background_tasks: BackgroundTasks,
    cache: Annotated[Pipeline, Depends(get_cache)],
    page_limit: Optional[int] = None,
    proxy: Optional[str] = None,
) -> Response:
    if page_limit is not None and page_limit <= 0:
        raise HTTPException(status_code=400, detail="Page limit must be a positive integer")
    local_storage = LocalStorage(path="./storage.json")
    notification = ConsoleNotification()
    object_storage = LocalObjectStorage(root_dir="./images")
    scrapper = Scrapper(
        storage=local_storage,
        cache=RedisCacheStorage(cache),
        proxy=proxy,
        notification=notification,
        object_storage=object_storage,
    )
    background_tasks.add_task(scrapper.scrap, user_id="user1", page_limit=page_limit)
    return Response(status_code=http.HTTPStatus.ACCEPTED)


__all__ = ["router"]
