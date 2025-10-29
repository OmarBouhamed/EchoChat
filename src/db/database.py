# src/db/database.py
from __future__ import annotations

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from sqlalchemy import text

from src.config import get_settings
from src.core.logger import logger

settings = get_settings()

def _ensure_async_url(url: str) -> str:
    """
    Ensure the SQLAlchemy URL uses an async dialect.
    - postgresql://...         -> postgresql+asyncpg://...
    - postgresql+psycopg://... -> postgresql+psycopg_async://...  (if you use psycopg3 async)
    """
    if url.startswith("postgresql://"):
        return "postgresql+asyncpg://" + url.split("postgresql://", 1)[1]
    if url.startswith("postgresql+psycopg://"):
        return "postgresql+psycopg_async://" + url.split("postgresql+psycopg://", 1)[1]
    # For SQLite, use: sqlite+aiosqlite:///path.db
    if url.startswith("sqlite:///"):
        return "sqlite+aiosqlite://" + url.split("sqlite://", 1)[1]
    return url

ASYNC_DB_URL = _ensure_async_url(settings.database_url)

# Create async engine
engine: AsyncEngine = create_async_engine(
    ASYNC_DB_URL,
    echo=bool(settings.database_echo),
    pool_pre_ping=True,
    # Use NullPool in dev to avoid containerized connection reuse issues / hot-reload quirks.
    poolclass=NullPool if settings.environment == "development" else None,
    # Tip: in prod you can also set pool_size / max_overflow via create_engine kwargs if not using NullPool.
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    # autocommit removed in SQLAlchemy 2.0; transactions are explicit
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an AsyncSession with proper cleanup."""
    async with AsyncSessionLocal() as session:
        yield session

async def init_db() -> None:
    """Initialize database (create tables) and validate connectivity."""
    from src.db.models import Base  # import here to avoid circulars

    # 1) Migrations > create_all. If you use Alembic, prefer running migrations instead.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2) Connectivity sanity check with a lightweight query
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        logger.exception("❌ Database connectivity check failed")
        raise
    else:
        logger.info("✅ Database initialized and connectivity verified")

async def close_db() -> None:
    """Close database connections and dispose the engine."""
    await engine.dispose()
    logger.info("✅ Database closed")
