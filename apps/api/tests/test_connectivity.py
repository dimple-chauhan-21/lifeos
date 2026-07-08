import asyncpg
import redis.asyncio as redis
from minio import Minio

from app.core.config import get_settings


async def test_can_reach_postgres() -> None:
    settings = get_settings()
    conn = await asyncpg.connect(settings.database_url)
    try:
        assert await conn.fetchval("SELECT 1") == 1
    finally:
        await conn.close()


async def test_can_reach_redis() -> None:
    settings = get_settings()
    client = redis.from_url(settings.redis_url)
    try:
        assert await client.ping() is True
    finally:
        await client.aclose()


def test_can_reach_minio() -> None:
    settings = get_settings()
    client = Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )
    # A real round trip to the server, not just client construction.
    client.list_buckets()
