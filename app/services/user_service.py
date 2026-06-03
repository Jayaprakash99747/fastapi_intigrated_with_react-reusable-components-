from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.services.auth_service import auth_service


class UserService:

    # =====================================================
    # GET CURRENT USER
    # =====================================================

    async def get_user(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> Optional[User]:

        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # UPDATE PROFILE
    # =====================================================

    async def update_profile(
        self,
        db: AsyncSession,
        user: User,
        **kwargs,
    ) -> User:

        allowed_fields = [
            "username",
            "phone",
            "address",
            "city",
            "state",
            "pincode",
            "profile_image",
        ]

        for key, value in kwargs.items():
            if key in allowed_fields and value is not None:
                setattr(user, key, value)

        await db.commit()
        await db.refresh(user)

        return user

    # =====================================================
    # CHANGE PASSWORD
    # =====================================================

    async def change_password(
        self,
        db: AsyncSession,
        user: User,
        old_password: str,
        new_password: str,
    ) -> bool:

        # verify old password
        if not auth_service.verify_password(old_password, user.password):
            return False

        # update password
        user.password = auth_service.hash_password(new_password)

        await db.commit()

        return True

    # =====================================================
    # UPDATE EMAIL
    # =====================================================

    async def update_email(
        self,
        db: AsyncSession,
        user: User,
        new_email: str,
    ) -> User:

        user.email = new_email
        user.is_email_verified = False  # reset verification

        await db.commit()
        await db.refresh(user)

        return user

    # =====================================================
    # DELETE ACCOUNT (SOFT DELETE READY)
    # =====================================================

    async def delete_account(
        self,
        db: AsyncSession,
        user: User,
    ) -> bool:

        user.is_active = False

        await db.commit()

        return True

    # =====================================================
    # LIST USERS (ADMIN ONLY)
    # =====================================================

    async def list_users(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
    ) -> List[User]:

        stmt = select(User).offset(skip).limit(limit)

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # ACTIVATE / DEACTIVATE USER (ADMIN)
    # =====================================================

    async def toggle_user_status(
        self,
        db: AsyncSession,
        user: User,
    ) -> User:

        user.is_active = not user.is_active

        await db.commit()
        await db.refresh(user)

        return user

    # =====================================================
    # VERIFY EMAIL
    # =====================================================

    async def verify_email(
        self,
        db: AsyncSession,
        user: User,
    ) -> User:

        user.is_email_verified = True

        await db.commit()
        await db.refresh(user)

        return user

    # =====================================================
    # USER STATS (ADMIN DASHBOARD)
    # =====================================================

    async def user_stats(self, db: AsyncSession):

        stmt = select(User)
        result = await db.execute(stmt)

        users = result.scalars().all()

        total_users = len(users)
        active_users = len([u for u in users if u.is_active])
        verified_users = len([u for u in users if u.is_email_verified])

        return {
            "total_users": total_users,
            "active_users": active_users,
            "verified_users": verified_users,
        }


user_service = UserService()