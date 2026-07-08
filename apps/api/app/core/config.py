from functools import lru_cache
from urllib.parse import urlparse

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_name: str
    minio_secure: bool = False

    @field_validator("database_url")
    @classmethod
    def _validate_database_url(cls, v: str) -> str:
        if urlparse(v).scheme not in ("postgresql", "postgres"):
            raise ValueError("database_url must be a postgresql:// URL")
        return v

    @field_validator("redis_url")
    @classmethod
    def _validate_redis_url(cls, v: str) -> str:
        if urlparse(v).scheme != "redis":
            raise ValueError("redis_url must be a redis:// URL")
        return v

    @field_validator(
        "minio_endpoint", "minio_access_key", "minio_secret_key", "minio_bucket_name"
    )
    @classmethod
    def _validate_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must not be blank")
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
