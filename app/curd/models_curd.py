from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    hashed = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        password=hashed,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user