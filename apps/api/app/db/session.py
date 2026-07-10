from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import get_settings

_settings = get_settings()

# Settings.database_url validates a generic postgresql:// URL; the async
# driver is an infrastructure detail, not something callers should have to
# spell out in DATABASE_URL themselves.
_async_database_url = _settings.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(_async_database_url)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
