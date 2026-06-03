from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_write_engine, database_health_check
from app.core.settings import settings
from app.core.security import hash_password
from app.core.config import logger
from app.db.base import Base
from app.models.user import User, UserRole


# --------------------------
# CREATE TABLES
# --------------------------
async def create_tables():
    logger.info("Creating database tables")

    engine = get_write_engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Tables created")


# --------------------------
# SEED ADMIN (NO DB PARAM)
# --------------------------
async def create_admin_user():
    from app.core.database import AsyncWriteSessionLocal

    async with AsyncWriteSessionLocal() as db:

        result = await db.execute(
            User.__table__.select().where(User.email == settings.ADMIN_EMAIL)
        )

        admin = result.scalar_one_or_none()

        if admin:
            return

        admin_user = User(
            username=settings.ADMIN_NAME,
            email=settings.ADMIN_EMAIL,
            password=hash_password(settings.ADMIN_PASSWORD),
            role=UserRole.ADMIN,
            is_active=True,
            is_email_verified=True,
        )

        db.add(admin_user)
        await db.commit()


# --------------------------
# INIT DB (NO PARAMS)
# --------------------------
async def init_db():
    logger.info("Initializing database...")

    await create_tables()
    await create_admin_user()

    logger.info("DB initialized")













# from sqlalchemy.ext.asyncio import AsyncSession
# from app.models import User, UserRole
# from app.core.security import get_password_hash

# async def init_db(db: AsyncSession):
#     # Check if admin exists
#     result = await db.execute(
#         "SELECT id FROM users WHERE role = :role LIMIT 1",
#         {"role": UserRole.ADMIN}
#     )
#     if not result.scalar_one_or_none():
#         admin_user = User(
#             username="admin",
#             email="admin@ecom.com",
#             password=get_password_hash("admin123"),
#             role=UserRole.ADMIN,
#             is_active=True,
#             is_email_verified=True
#         )
#         db.add(admin_user)
#         await db.commit()











# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.core.database import (
#     Base,
#     get_write_engine,
#     database_health_check,
# )
# from app.core.settings import settings
# from app.core.security import hash_password
# from app.core.config import logger

# # Import all models
# from app.db.base import *

# from app.models.user import User
# from app.models.user import UserRole

# # ==========================================================
# # CREATE TABLES
# # ==========================================================

# async def create_tables() -> None:
#     """
#     Create all tables.

#     Production:
#     Normally use Alembic migrations.

#     Useful for:
#     - local development
#     - testing
#     - first deployment
#     """

#     logger.info("Creating database tables")

#     engine = get_write_engine()

#     async with engine.begin() as conn:
#         await conn.run_sync(
#             Base.metadata.create_all
#         )

#     logger.info("Database tables created")


# # ==========================================================
# # DROP TABLES
# # ==========================================================

# async def drop_tables() -> None:
#     """
#     Development only.
#     Never expose in production.
#     """

#     logger.warning(
#         "Dropping database tables"
#     )

#     engine = get_write_engine()

#     async with engine.begin() as conn:
#         await conn.run_sync(
#             Base.metadata.drop_all
#         )

#     logger.warning(
#         "Database tables dropped"
#     )


# # ==========================================================
# # SEED ADMIN USER
# # ==========================================================

# async def create_admin_user(
#     db: AsyncSession,
# ) -> None:

#     stmt = select(User).where(
#         User.email == settings.ADMIN_EMAIL
#     )

#     result = await db.execute(stmt)

#     admin = result.scalar_one_or_none()

#     if admin:
#         logger.info(
#             "Admin user already exists"
#         )
#         return

#     admin_user = User(
#         username=settings.ADMIN_USERNAME,
#         email=settings.ADMIN_EMAIL,
#         password=hash_password(
#             settings.ADMIN_PASSWORD
#         ),
#         role=UserRole.ADMIN,
#         is_active=True,
#         is_email_verified=True,
#     )

#     db.add(admin_user)

#     await db.commit()

#     logger.info(
#         "Admin user created"
#     )


# # ==========================================================
# # DEFAULT CATEGORIES
# # ==========================================================

# async def seed_categories(
#     db: AsyncSession,
# ):

#     try:
#         from app.models.product import Category

#         default_categories = [
#             "Electronics",
#             "Fashion",
#             "Books",
#             "Home",
#             "Mobiles",
#             "Sports",
#             "Beauty",
#             "Toys",
#         ]

#         for category_name in default_categories:

#             stmt = select(Category).where(
#                 Category.name == category_name
#             )

#             result = await db.execute(stmt)

#             exists = result.scalar_one_or_none()

#             if exists:
#                 continue

#             db.add(
#                 Category(
#                     name=category_name,
#                 )
#             )

#         await db.commit()

#         logger.info(
#             "Default categories seeded"
#         )

#     except Exception as exc:

#         logger.error(
#             f"Category seed failed: {exc}"
#         )


# # ==========================================================
# # DATABASE HEALTH CHECK
# # ==========================================================

# async def check_database() -> bool:

#     healthy = await database_health_check()

#     if healthy:

#         logger.info(
#             "Database health check passed"
#         )

#         return True

#     logger.error(
#         "Database health check failed"
#     )

#     return False


# # ==========================================================
# # STARTUP CHECKS
# # ==========================================================

# async def run_startup_checks():

#     logger.info(
#         "Running startup checks"
#     )

#     healthy = await check_database()

#     if not healthy:
#         raise RuntimeError(
#             "Database unavailable"
#         )

#     logger.info(
#         "Startup checks passed"
#     )


# # ==========================================================
# # INITIALIZE DATABASE
# # ==========================================================

# async def initialize_database(
#     db: AsyncSession,
# ):

#     logger.info(
#         "Initializing database"
#     )

#     await create_admin_user(db)

#     await seed_categories(db)

#     logger.info(
#         "Database initialization completed"
#     )


# # ==========================================================
# # FULL APPLICATION INIT
# # ==========================================================

# async def startup_database(
#     db: AsyncSession,
# ):

#     await run_startup_checks()

#     if settings.AUTO_CREATE_TABLES:
#         await create_tables()

#     await initialize_database(db)

#     logger.info(
#         "Database startup completed"
#     )


# # ==========================================================
# # SHUTDOWN
# # ==========================================================

# async def shutdown_database():

#     logger.info(
#         "Database shutdown completed"
#     )


# # ==========================================================
# # RESET DATABASE
# # ==========================================================

# async def reset_database(
#     db: AsyncSession,
# ):

#     logger.warning(
#         "Database reset started"
#     )

#     await drop_tables()

#     await create_tables()

#     await initialize_database(db)

#     logger.warning(
#         "Database reset completed"
#     )