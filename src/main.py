from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application")
    yield
    print("Shutting down application")


app = FastAPI(lifespan=lifespan)

app.include_router(router)

__all__ = ["app"]
