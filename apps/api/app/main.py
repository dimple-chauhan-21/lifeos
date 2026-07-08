from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    get_settings()  # fail fast: crash startup if configuration is missing or invalid
    yield


app = FastAPI(title="LifeOS API", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
