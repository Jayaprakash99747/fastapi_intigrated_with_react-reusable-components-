# from sqlalchemy.ext.asyncio import AsyncSession
# from app.core.database import AsyncSessionLocal

# async def get_db() -> AsyncSession:
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#         finally:
#             await session.close()






from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncWriteSessionLocal, AsyncReadSessionLocal


# ==========================================================
# MAIN DB DEPENDENCY (USE THIS IN ROUTERS)
# ==========================================================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Default FastAPI dependency (WRITE SESSION SAFE)
    """
    session = AsyncWriteSessionLocal()

    try:
        yield session
        await session.commit()

    except Exception:
        await session.rollback()
        raise

    finally:
        await session.close()


# ==========================================================
# READ ONLY SESSION (OPTIONAL)
# ==========================================================

async def get_read_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Read-only DB dependency
    """
    session = AsyncReadSessionLocal()

    try:
        yield session
    finally:
        await session.close()


# ==========================================================
# TRANSACTION CONTEXT (OPTIONAL ADVANCED USAGE)
# ==========================================================

@asynccontextmanager
async def transaction() -> AsyncGenerator[AsyncSession, None]:
    """
    Manual transaction context
    """
    session = AsyncWriteSessionLocal()

    try:
        yield session
        await session.commit()

    except Exception:
        await session.rollback()
        raise

    finally:
        await session.close()


# ==========================================================
# BULK TRANSACTION
# ==========================================================

@asynccontextmanager
async def bulk_transaction() -> AsyncGenerator[AsyncSession, None]:
    """
    Bulk operations transaction
    """
    session = AsyncWriteSessionLocal()

    try:
        yield session
        await session.commit()

    except Exception:
        await session.rollback()
        raise

    finally:
        await session.close()



# from contextlib import asynccontextmanager
# from typing import AsyncGenerator

# from sqlalchemy.ext.asyncio import AsyncSession

# from app.core.database import (
#     AsyncWriteSessionLocal,
#     AsyncReadSessionLocal,
# )


# # ==========================================================
# # WRITE SESSION
# # ==========================================================

# @asynccontextmanager
# async def get_write_session() -> AsyncGenerator[AsyncSession, None]:
#     """
#     Write session.

#     Used for:
#     - INSERT
#     - UPDATE
#     - DELETE
#     """

#     session = AsyncWriteSessionLocal()

#     try:
#         yield session

#         await session.commit()

#     except Exception:
#         await session.rollback()
#         raise

#     finally:
#         await session.close()


# # ==========================================================
# # READ SESSION
# # ==========================================================

# @asynccontextmanager
# async def get_read_session() -> AsyncGenerator[AsyncSession, None]:
#     """
#     Read session.

#     Used for:
#     - SELECT
#     """

#     session = AsyncReadSessionLocal()

#     try:
#         yield session

#     finally:
#         await session.close()


# # ==========================================================
# # UNIT OF WORK
# # ==========================================================

# class UnitOfWork:
#     """
#     Production Unit Of Work Pattern

#     Example:

#     async with UnitOfWork() as uow:

#         user = User(...)
#         uow.session.add(user)

#         await uow.commit()
#     """

#     def __init__(self):
#         self.session: AsyncSession | None = None

#     async def __aenter__(self):
#         self.session = AsyncWriteSessionLocal()
#         return self

#     async def __aexit__(
#         self,
#         exc_type,
#         exc_val,
#         exc_tb,
#     ):

#         if exc_type:
#             await self.rollback()

#         await self.close()

#     async def commit(self):
#         await self.session.commit()

#     async def rollback(self):
#         await self.session.rollback()

#     async def flush(self):
#         await self.session.flush()

#     async def refresh(self, obj):
#         await self.session.refresh(obj)

#     async def close(self):
#         await self.session.close()


# # ==========================================================
# # TRANSACTION MANAGER
# # ==========================================================

# @asynccontextmanager
# async def transaction():
#     """
#     Manual transaction.

#     Example:

#     async with transaction() as db:

#         db.add(obj)

#         await db.flush()
#     """

#     session = AsyncWriteSessionLocal()

#     try:
#         yield session

#         await session.commit()

#     except Exception:
#         await session.rollback()
#         raise

#     finally:
#         await session.close()


# # ==========================================================
# # READ ONLY TRANSACTION
# # ==========================================================

# @asynccontextmanager
# async def readonly_transaction():
#     """
#     Read-only transaction.
#     """

#     session = AsyncReadSessionLocal()

#     try:
#         yield session

#     finally:
#         await session.close()


# # ==========================================================
# # SESSION FACTORY
# # ==========================================================

# class SessionFactory:

#     @staticmethod
#     async def write() -> AsyncSession:
#         return AsyncWriteSessionLocal()

#     @staticmethod
#     async def read() -> AsyncSession:
#         return AsyncReadSessionLocal()


# # ==========================================================
# # SESSION MANAGER
# # ==========================================================

# class SessionManager:

#     @staticmethod
#     async def commit(session: AsyncSession):
#         await session.commit()

#     @staticmethod
#     async def rollback(session: AsyncSession):
#         await session.rollback()

#     @staticmethod
#     async def flush(session: AsyncSession):
#         await session.flush()

#     @staticmethod
#     async def refresh(
#         session: AsyncSession,
#         instance,
#     ):
#         await session.refresh(instance)

#     @staticmethod
#     async def close(session: AsyncSession):
#         await session.close()


# # ==========================================================
# # BULK TRANSACTION
# # ==========================================================

# @asynccontextmanager
# async def bulk_transaction():
#     """
#     Bulk insert/update transaction.

#     Example:

#     async with bulk_transaction() as db:

#         db.add_all(objects)
#     """

#     session = AsyncWriteSessionLocal()

#     try:
#         yield session

#         await session.commit()

#     except Exception:
#         await session.rollback()
#         raise

#     finally:
#         await session.close()


# # ==========================================================
# # NESTED TRANSACTION
# # ==========================================================

# @asynccontextmanager
# async def nested_transaction():
#     """
#     Savepoint transaction.

#     Example:

#     async with nested_transaction() as db:
#         ...
#     """

#     session = AsyncWriteSessionLocal()

#     try:

#         async with session.begin_nested():

#             yield session

#         await session.commit()

#     except Exception:

#         await session.rollback()

#         raise

#     finally:

#         await session.close()


# # ==========================================================
# # HEALTH CHECK SESSION
# # ==========================================================

# async def health_session() -> AsyncSession:
#     """
#     Used by health endpoints.
#     """
#     return AsyncReadSessionLocal()


# # ==========================================================
# # EXPORTS
# # ==========================================================

# __all__ = [
#     "UnitOfWork",
#     "transaction",
#     "readonly_transaction",
#     "bulk_transaction",
#     "nested_transaction",
#     "SessionFactory",
#     "SessionManager",
#     "get_write_session",
#     "get_read_session",
# ]