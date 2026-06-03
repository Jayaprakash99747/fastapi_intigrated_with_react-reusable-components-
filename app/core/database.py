# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
# from sqlalchemy.orm import DeclarativeBase
# from app.core.settings import settings


# engine = create_async_engine(
#     settings.DATABASE_URL,
#     echo=settings.DEBUG,
#     pool_pre_ping=True,
#     pool_size=10,
#     max_overflow=20,
# )

# AsyncSessionLocal = async_sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
#     autoflush=False,
#     autocommit=False,
# )


# class Base(DeclarativeBase):
#     pass


# async def get_db() -> AsyncSession:
#     """Dependency that provides a database session."""
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#             await session.commit()
#         except Exception:
#             await session.rollback()
#             raise
#         finally:
#             await session.close()







import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.exc import OperationalError, DisconnectionError

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import settings


# ==========================================================
# WRITE DATABASE ENGINE
# ==========================================================

write_engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True,
    pool_pre_ping=True,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_recycle=settings.DATABASE_POOL_RECYCLE,
    pool_use_lifo=True,
)


# ==========================================================
# READ DATABASE ENGINE
# ==========================================================

read_engine: AsyncEngine = create_async_engine(
    settings.READ_DATABASE_URL
    if settings.READ_DATABASE_URL
    else settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_recycle=settings.DATABASE_POOL_RECYCLE,
    pool_use_lifo=True,
)


# ==========================================================
# SESSION FACTORIES
# ==========================================================

AsyncWriteSessionLocal = async_sessionmaker(
    bind=write_engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
    class_=AsyncSession,
)

AsyncReadSessionLocal = async_sessionmaker(
    bind=read_engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
    class_=AsyncSession,
)


# ==========================================================
# RETRY CONNECTION
# ==========================================================

async def wait_for_database(
    retries: int = 10,
    delay: int = 5,
):
    """
    Used during startup.
    Waits until PostgreSQL becomes available.
    """

    for attempt in range(retries):
        try:
            async with write_engine.begin() as conn:
                await conn.execute(text("SELECT 1"))

            print("Database Connected")
            return

        except Exception as exc:
            print(
                f"Database unavailable. Retry {attempt + 1}/{retries}"
            )

            if attempt == retries - 1:
                raise exc

            await asyncio.sleep(delay)


# ==========================================================
# WRITE SESSION DEPENDENCY
# ==========================================================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Default DB session.
    Used for create/update/delete.
    """

    async with AsyncWriteSessionLocal() as session:
        try:
            yield session

            await session.commit()

        except Exception:
            await session.rollback()
            raise

        finally:
            await session.close()


# ==========================================================
# READ SESSION DEPENDENCY
# ==========================================================

async def get_read_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Read replica session.
    Used for GET endpoints.
    """

    async with AsyncReadSessionLocal() as session:
        try:
            yield session

        finally:
            await session.close()


# ==========================================================
# TRANSACTION MANAGER
# ==========================================================

@asynccontextmanager
async def transaction():
    """
    Manual transaction.

    Example:

    async with transaction() as db:
        ...
    """

    async with AsyncWriteSessionLocal() as session:

        try:
            yield session

            await session.commit()

        except Exception:
            await session.rollback()
            raise

        finally:
            await session.close()


# ==========================================================
# HEALTH CHECK
# ==========================================================

async def database_health_check() -> bool:
    """
    Used in health endpoint.
    """

    try:
        async with AsyncReadSessionLocal() as session:

            result = await session.execute(
                text("SELECT 1")
            )

            value = result.scalar()

            return value == 1

    except Exception:
        return False


# ==========================================================
# ENGINE ACCESSORS
# ==========================================================

def get_write_engine() -> AsyncEngine:
    return write_engine


def get_read_engine() -> AsyncEngine:
    return read_engine


# ==========================================================
# DATABASE SHUTDOWN
# ==========================================================

async def close_database_connections():
    """
    FastAPI shutdown event.
    """

    await write_engine.dispose()

    if read_engine != write_engine:
        await read_engine.dispose()


# ==========================================================
# RAW QUERY EXECUTOR
# ==========================================================

async def execute_raw_query(
    query: str,
    params: dict | None = None,
):
    """
    Execute raw SQL safely.
    """

    async with AsyncWriteSessionLocal() as session:

        result = await session.execute(
            text(query),
            params or {},
        )

        await session.commit()

        return result


# ==========================================================
# DATABASE PING
# ==========================================================

async def ping_database() -> bool:
    try:
        async with write_engine.connect() as conn:

            await conn.execute(
                text("SELECT 1")
            )

        return True

    except (
        OperationalError,
        DisconnectionError,
        Exception,
    ):
        return False


# ==========================================================
# STARTUP INITIALIZATION
# ==========================================================

async def initialize_database():
    """
    Called during FastAPI startup.
    """

    await wait_for_database()

    if not await ping_database():
        raise RuntimeError(
            "Database connection failed"
        )

    print("Database initialized successfully")