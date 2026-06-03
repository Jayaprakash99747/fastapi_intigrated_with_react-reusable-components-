from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import (
    User,
    RefreshToken,
    PasswordResetCode,
)


class UserCRUD:

    # =====================================================
    # CREATE USER
    # =====================================================

    async def create_user(
        self,
        db: AsyncSession,
        **kwargs
    ) -> User:

        user = User(**kwargs)

        db.add(user)

        await db.commit()

        await db.refresh(user)

        return user

    # =====================================================
    # GET USER BY ID
    # =====================================================

    async def get_by_id(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> User | None:

        query = (
            select(User)
            .options(
                selectinload(User.refresh_tokens)
            )
            .where(
                User.id == user_id,
                User.is_active.is_(True),
            )
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()

    # =====================================================
    # GET USER BY EMAIL
    # =====================================================

    async def get_by_email(
        self,
        db: AsyncSession,
        email: str,
    ) -> User | None:

        query = (
            select(User)
            .where(
                User.email == email
            )
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()

    # =====================================================
    # GET USER BY USERNAME
    # =====================================================

    async def get_by_username(
        self,
        db: AsyncSession,
        username: str,
    ) -> User | None:

        query = (
            select(User)
            .where(
                User.username == username
            )
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()

    # =====================================================
    # GET USER BY PHONE
    # =====================================================

    async def get_by_phone(
        self,
        db: AsyncSession,
        phone: str,
    ) -> User | None:

        query = (
            select(User)
            .where(
                User.phone == phone
            )
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()

    # =====================================================
    # UPDATE USER
    # =====================================================

    async def update_user(
        self,
        db: AsyncSession,
        user: User,
        **kwargs
    ) -> User:

        for key, value in kwargs.items():
            setattr(user, key, value)

        user.updated_at = datetime.utcnow()

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
        hashed_password: str,
    ) -> User:

        user.password = hashed_password

        user.updated_at = datetime.utcnow()

        await db.commit()

        await db.refresh(user)

        return user

    # =====================================================
    # SOFT DELETE USER
    # =====================================================

    async def soft_delete(
        self,
        db: AsyncSession,
        user: User,
    ) -> None:

        user.is_active = False

        user.updated_at = datetime.utcnow()

        await db.commit()

    # =====================================================
    # HARD DELETE USER
    # =====================================================

    async def hard_delete(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> None:

        stmt = (
            delete(User)
            .where(User.id == user_id)
        )

        await db.execute(stmt)

        await db.commit()

    # =====================================================
    # STORE REFRESH TOKEN
    # =====================================================

    async def create_refresh_token(
        self,
        db: AsyncSession,
        user_id: int,
        token: str,
        expires_at,
    ) -> RefreshToken:

        refresh = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )

        db.add(refresh)

        await db.commit()

        await db.refresh(refresh)

        return refresh

    # =====================================================
    # GET REFRESH TOKEN
    # =====================================================

    async def get_refresh_token(
        self,
        db: AsyncSession,
        token: str,
    ) -> RefreshToken | None:

        query = (
            select(RefreshToken)
            .where(
                RefreshToken.token == token,
                RefreshToken.is_revoked.is_(False),
            )
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()

    # =====================================================
    # REVOKE REFRESH TOKEN
    # =====================================================

    async def revoke_refresh_token(
        self,
        db: AsyncSession,
        token: str,
    ) -> None:

        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.token == token
            )
            .values(
                is_revoked=True
            )
        )

        await db.execute(stmt)

        await db.commit()

    # =====================================================
    # REVOKE ALL USER TOKENS
    # =====================================================

    async def revoke_all_user_tokens(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> None:

        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id
            )
            .values(
                is_revoked=True
            )
        )

        await db.execute(stmt)

        await db.commit()

    # =====================================================
    # CREATE RESET CODE
    # =====================================================

    async def create_reset_code(
        self,
        db: AsyncSession,
        user_id: int,
        code: str,
        expires_at,
    ) -> PasswordResetCode:

        reset = PasswordResetCode(
            user_id=user_id,
            reset_code=code,
            expires_at=expires_at,
        )

        db.add(reset)

        await db.commit()

        await db.refresh(reset)

        return reset

    # =====================================================
    # GET VALID RESET CODE
    # =====================================================

    async def get_valid_reset_code(
        self,
        db: AsyncSession,
        user_id: int,
        code: str,
    ) -> PasswordResetCode | None:

        query = (
            select(PasswordResetCode)
            .where(
                PasswordResetCode.user_id == user_id,
                PasswordResetCode.reset_code == code,
                PasswordResetCode.is_used.is_(False),
            )
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()

    # =====================================================
    # MARK RESET CODE USED
    # =====================================================

    async def mark_reset_code_used(
        self,
        db: AsyncSession,
        reset_code: PasswordResetCode,
    ) -> None:

        reset_code.is_used = True

        await db.commit()

    # =====================================================
    # LIST USERS
    # =====================================================

    async def get_users(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
    ):

        query = (
            select(User)
            .offset(skip)
            .limit(limit)
            .order_by(User.id.desc())
        )

        result = await db.execute(query)

        return result.scalars().all()

    # =====================================================
    # TOTAL USERS
    # =====================================================

    async def count_users(
        self,
        db: AsyncSession,
    ):

        query = select(User)

        result = await db.execute(query)

        return len(result.scalars().all())


user_crud = UserCRUD()