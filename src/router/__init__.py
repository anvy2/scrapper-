from fastapi import APIRouter
from src.router.scrapper import router as scrapper_router

router = APIRouter()
router.include_router(scrapper_router)

__all__ = ["router"]
