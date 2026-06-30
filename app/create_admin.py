import asyncio

from sqlalchemy import select

from app.core.database import AsyncWriteSessionLocal
from app.core.security import hash_password
from app.core.constants import UserRole

from app.models.user import User


async def create_admin():

    async with AsyncWriteSessionLocal() as db:

        result = await db.execute(
            select(User).where(
                User.email == "admin2@example.com"
            )
        )

        existing = result.scalar_one_or_none()

        if existing:
            print("Admin already exists")
            return

        admin = User(
            username="admin2",
            email="admin2@example.com",
            password=hash_password("Admin@123"),
            role=UserRole.ADMIN,
            is_active=True,
            is_email_verified=True,
        )

        db.add(admin)

        await db.commit()

        await db.refresh(admin)

        print("Admin created successfully")
        print(f"Email: {admin.email}")
        print("Password: Admin@123")


if __name__ == "__main__":
    asyncio.run(create_admin())



# then run:

# python -m app.create_admin