import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from app.db.base import Base
from app.db.session import engine as _app_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# The project's own declarative Base — models register against this via
# app.db.base.Base, so autogenerate sees them without a second, duplicate
# metadata declaration here.
target_metadata = Base.metadata

# DATABASE_URL has exactly one source of truth: Settings, via
# app.db.session's existing postgresql:// -> postgresql+asyncpg:// scheme
# conversion. Reused here as a plain string only — Alembic still builds its
# own independent Engine below (see run_async_migrations), per Alembic's
# own official async recipe, rather than reusing the application's engine
# and its connection pool. hide_password=False is required: str(URL) masks
# the password with "***" by default (a SQLAlchemy safety default against
# accidental credential leakage in logs), which is correct for display but
# unusable for an actual connection — caught only by actually connecting.
_database_url = _app_engine.url.render_as_string(hide_password=False)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=_database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Build a dedicated engine for migrations, independent of the
    application's — per Alembic's official async recipe, using NullPool
    since a one-shot CLI process has no use for connection pooling and
    shouldn't hold pooled connections open after it exits.
    """
    connectable = create_async_engine(_database_url, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
