# from datetime import datetime, timedelta
# from typing import Optional, Union
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from fastapi import HTTPException, status
# from app.core.settings import settings
# from app.core.constants import MSG_INVALID_TOKEN

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def hash_password(password: str) -> str:
#     """Hash a plain password using bcrypt."""
#     return pwd_context.hash(password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """Verify a plain password against its hash."""
#     return pwd_context.verify(plain_password, hashed_password)


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
#     """Create a JWT access token."""
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (
#         expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     )
#     to_encode.update({"exp": expire, "type": "access"})
#     return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# def create_refresh_token(data: dict) -> str:
#     """Create a JWT refresh token."""
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
#     to_encode.update({"exp": expire, "type": "refresh"})
#     return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# def decode_token(token: str) -> dict:
#     """Decode and validate a JWT token."""
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         return payload
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=MSG_INVALID_TOKEN,
#             headers={"WWW-Authenticate": "Bearer"},
#         )


# def verify_access_token(token: str) -> dict:
#     payload = decode_token(token)
#     if payload.get("type") != "access":
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=MSG_INVALID_TOKEN,
#         )
#     return payload


# def verify_refresh_token(token: str) -> dict:
#     payload = decode_token(token)
#     if payload.get("type") != "refresh":
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid refresh token",
#         )
#     return payload


# def generate_reset_code(length: int = 6) -> str:
#     """Generate a numeric OTP reset code."""
#     import random
#     return "".join([str(random.randint(0, 9)) for _ in range(length)])













from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from redis.asyncio import Redis

from app.core.settings import settings
from app.core.constants import (
    REDIS_BLACKLIST_TOKEN,
    TokenType,
)


# ==========================================================
# PASSWORD HASHING
# ==========================================================

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    Hash password using Argon2.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify password.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ==========================================================
# RSA KEYS
# ==========================================================

def _load_private_key() -> str:
    private_key_path = Path(
        settings.PRIVATE_KEY_PATH
    )

    if not private_key_path.exists():
        raise RuntimeError(
            f"Private key not found: "
            f"{private_key_path}"
        )

    return private_key_path.read_text()


def _load_public_key() -> str:
    public_key_path = Path(
        settings.PUBLIC_KEY_PATH
    )

    if not public_key_path.exists():
        raise RuntimeError(
            f"Public key not found: "
            f"{public_key_path}"
        )

    return public_key_path.read_text()


PRIVATE_KEY = None
PUBLIC_KEY = None

if settings.JWT_ALGORITHM == "RS256":
    PRIVATE_KEY = _load_private_key()
    PUBLIC_KEY = _load_public_key()


# ==========================================================
# TOKEN CREATION
# ==========================================================

def _create_token(
    *,
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    extra_data: Optional[dict] = None,
) -> str:

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(subject),
        "type": token_type,
        "iat": now,
        "nbf": now,
        "exp": now + expires_delta,
    }

    if extra_data:
        payload.update(extra_data)

    key = PRIVATE_KEY if settings.JWT_ALGORITHM == "RS256" else settings.SECRET_KEY

    token = jwt.encode(
        payload,
        key,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token


def create_access_token(
    user_id: int,
    role: str,
) -> str:

    return _create_token(
        subject=str(user_id),
        token_type=TokenType.ACCESS.value,
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        extra_data={
            "role": role,
        },
    )


def create_refresh_token(
    user_id: int,
) -> str:

    return _create_token(
        subject=str(user_id),
        token_type=TokenType.REFRESH.value,
        expires_delta=timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        ),
    )


def create_email_verification_token(
    user_id: int,
) -> str:

    return _create_token(
        subject=str(user_id),
        token_type=TokenType.EMAIL_VERIFICATION.value,
        expires_delta=timedelta(
            hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS
        ),
    )


def create_password_reset_token(
    user_id: int,
) -> str:

    return _create_token(
        subject=str(user_id),
        token_type=TokenType.PASSWORD_RESET.value,
        expires_delta=timedelta(
            minutes=settings.PASSWORD_RESET_EXPIRE_MINUTES
        ),
    )


# ==========================================================
# TOKEN VALIDATION
# ==========================================================

def decode_token(
    token: str,
) -> dict[str, Any]:

    try:

        payload = jwt.decode(
            token,
            key = PUBLIC_KEY if settings.JWT_ALGORITHM == "RS256" else settings.SECRET_KEY,
            algorithms=[
                settings.JWT_ALGORITHM
            ],
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def verify_token_type(
    payload: dict,
    token_type: str,
):

    if payload.get("type") != token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )


# ==========================================================
# ACCESS TOKEN
# ==========================================================

def verify_access_token(
    token: str,
) -> dict:

    payload = decode_token(token)

    verify_token_type(
        payload,
        TokenType.ACCESS.value,
    )

    return payload


# ==========================================================
# REFRESH TOKEN
# ==========================================================

def verify_refresh_token(
    token: str,
) -> dict:

    payload = decode_token(token)

    verify_token_type(
        payload,
        TokenType.REFRESH.value,
    )

    return payload


# ==========================================================
# PASSWORD RESET TOKEN
# ==========================================================

def verify_password_reset_token(
    token: str,
) -> dict:

    payload = decode_token(token)

    verify_token_type(
        payload,
        TokenType.PASSWORD_RESET.value,
    )

    return payload


# ==========================================================
# EMAIL VERIFY TOKEN
# ==========================================================

def verify_email_verification_token(
    token: str,
) -> dict:

    payload = decode_token(token)

    verify_token_type(
        payload,
        TokenType.EMAIL_VERIFICATION.value,
    )

    return payload


# ==========================================================
# TOKEN BLACKLIST
# ==========================================================

async def blacklist_token(
    redis: Redis,
    token: str,
    expires_in: int,
):

    key = REDIS_BLACKLIST_TOKEN.format(
        token
    )

    await redis.set(
        key,
        "1",
        ex=expires_in,
    )


async def is_token_blacklisted(
    redis: Redis,
    token: str,
) -> bool:

    key = REDIS_BLACKLIST_TOKEN.format(
        token
    )

    exists = await redis.exists(key)

    return bool(exists)


# ==========================================================
# REFRESH ROTATION
# ==========================================================

async def rotate_refresh_token(
    redis: Redis,
    old_token: str,
    user_id: int,
):

    payload = verify_refresh_token(
        old_token
    )

    exp = payload.get("exp")

    now = int(
        datetime.now(
            timezone.utc
        ).timestamp()
    )

    ttl = exp - now

    if ttl > 0:
        await blacklist_token(
            redis,
            old_token,
            ttl,
        )

    return create_refresh_token(
        user_id
    )


# ==========================================================
# TOKEN PAYLOAD HELPERS
# ==========================================================

def get_user_id_from_payload(
    payload: dict,
) -> int:

    sub = payload.get("sub")

    if not sub:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload",
        )

    return int(sub)


def get_role_from_payload(
    payload: dict,
) -> str:

    return payload.get(
        "role",
        "",
    )


# ==========================================================
# SECURITY UTILITIES
# ==========================================================

def generate_expiry_timestamp(
    minutes: int,
) -> datetime:

    return (
        datetime.now(
            timezone.utc
        )
        + timedelta(
            minutes=minutes
        )
    )


def generate_token_response(
    access_token: str,
    refresh_token: str,
):

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in":
            settings.ACCESS_TOKEN_EXPIRE_MINUTES
            * 60,
    }


# ==========================================================
# AUTHORIZATION HEADER
# ==========================================================

def extract_bearer_token(
    authorization: str,
) -> str:

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing",
        )

    try:
        scheme, token = authorization.split()

        if scheme.lower() != "bearer":
            raise ValueError()

        return token

    except ValueError:

        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header",
        )

# from jose import jwt, JWTError
# from app.core.logging_configuration import settings


# def decode_access_token(token: str):
#     try:
#         payload = jwt.decode(
#             token,
#             settings.SECRET_KEY,
#             algorithms=[settings.ALGORITHM]
#         )
#         return payload
#     except JWTError:
#         return None