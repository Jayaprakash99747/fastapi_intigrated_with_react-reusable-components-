# app/db/admin_seed.py

from sqlalchemy import select

from app.core.database import AsyncWriteSessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.core.constants import UserRole


async def create_admin_user():

    async with AsyncWriteSessionLocal() as db:

        result = await db.execute(
            select(User).where(
                User.email == "admin@example.com"
            )
        )

        admin = result.scalar_one_or_none()

        if admin:
            print("Admin already exists")
            return

        admin = User(
            username="Admin",
            email="admin@example.com",
            password=hash_password("Admin@123"),
            role=UserRole.ADMIN,
            is_active=True,
            is_email_verified=True,
        )

        db.add(admin)

        await db.commit()

        print("Admin user created successfully")