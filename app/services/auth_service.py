# from fastapi import HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.curd.models_curd import get_user_by_email, create_user
# from app.schemas.models_schemas import UserCreate
# from app.core.security import create_access_token, create_refresh_token, verify_password
# from app.models import RefreshToken

# async def register_user(db: AsyncSession, user_in: UserCreate):
#     if await get_user_by_email(db, user_in.email):
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return await create_user(db, user_in)

# async def authenticate_user(db: AsyncSession, email: str, password: str):
#     user = await get_user_by_email(db, email)
#     if not user or not verify_password(password, user.password):
#         return None
#     return user












from datetime import datetime, timedelta
from typing import Optional, Tuple

from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User, RefreshToken
from app.core.config import settings


# =====================================================
# PASSWORD HASHING (PRODUCTION GRADE)
# =====================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class AuthService:

    # =====================================================
    # HASH PASSWORD
    # =====================================================

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    # =====================================================
    # VERIFY PASSWORD
    # =====================================================

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # =====================================================
    # CREATE ACCESS TOKEN
    # =====================================================

    def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None,
    ) -> str:

        to_encode = data.copy()

        expire = datetime.utcnow() + (
            expires_delta
            or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        to_encode.update({"exp": expire, "type": "access"})

        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    # =====================================================
    # CREATE REFRESH TOKEN
    # =====================================================

    def create_refresh_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None,
    ) -> str:

        to_encode = data.copy()

        expire = datetime.utcnow() + (
            expires_delta
            or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )

        to_encode.update({"exp": expire, "type": "refresh"})

        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    # =====================================================
    # DECODE TOKEN
    # =====================================================

    def decode_token(self, token: str) -> dict:

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            return payload

        except JWTError:
            return {}

    # =====================================================
    # GET USER BY EMAIL
    # =====================================================

    async def get_user_by_email(
        self,
        db: AsyncSession,
        email: str,
    ) -> Optional[User]:

        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # GET USER BY ID
    # =====================================================

    async def get_user_by_id(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> Optional[User]:

        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # REGISTER USER
    # =====================================================

    async def register_user(
        self,
        db: AsyncSession,
        username: str,
        email: str,
        password: str,
    ) -> User:

        hashed_password = self.hash_password(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            is_active=True,
            is_email_verified=False,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    # =====================================================
    # LOGIN USER
    # =====================================================

    async def login_user(
        self,
        db: AsyncSession,
        email: str,
        password: str,
    ) -> Tuple[Optional[str], Optional[str], Optional[User]]:

        user = await self.get_user_by_email(db, email)

        if not user:
            return None, None, None

        if not self.verify_password(password, user.password):
            return None, None, None

        access_token = self.create_access_token(
            data={"sub": str(user.id), "role": user.role},
        )

        refresh_token = self.create_refresh_token(
            data={"sub": str(user.id)},
        )

        # Store refresh token in DB (production security)
        db_token = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.utcnow()
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        db.add(db_token)
        await db.commit()

        return access_token, refresh_token, user

    # =====================================================
    # REFRESH TOKEN
    # =====================================================

    async def refresh_access_token(
        self,
        db: AsyncSession,
        refresh_token: str,
    ) -> Optional[str]:

        payload = self.decode_token(refresh_token)

        if not payload or payload.get("type") != "refresh":
            return None

        user_id = payload.get("sub")

        stmt = select(RefreshToken).where(
            RefreshToken.token == refresh_token,
            RefreshToken.is_revoked.is_(False),
        )

        result = await db.execute(stmt)
        token_db = result.scalar_one_or_none()

        if not token_db:
            return None

        user = await self.get_user_by_id(db, int(user_id))

        if not user:
            return None

        return self.create_access_token(
            data={"sub": str(user.id), "role": user.role},
        )

    # =====================================================
    # LOGOUT USER
    # =====================================================

    async def logout_user(
        self,
        db: AsyncSession,
        refresh_token: str,
    ) -> bool:

        stmt = select(RefreshToken).where(
            RefreshToken.token == refresh_token
        )

        result = await db.execute(stmt)
        token_db = result.scalar_one_or_none()

        if token_db:
            token_db.is_revoked = True
            await db.commit()

            return True

        return False


auth_service = AuthService()