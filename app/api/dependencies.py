

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from redis.asyncio import Redis

from app.db.session import get_db
from app.db.redis import get_redis

from app.models.user import User, UserRole

from app.core.security import (
    verify_access_token,
    get_user_id_from_payload,
    is_token_blacklisted,
)


# =====================================================
# OAUTH2
# =====================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)


# =====================================================
# COMMON DEPENDENCIES
# =====================================================

DBSession = Annotated[
    AsyncSession,
    Depends(get_db)
]

RedisSession = Annotated[
    Redis,
    Depends(get_redis)
]


# =====================================================
# CURRENT USER
# =====================================================

# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: AsyncSession = Depends(get_db),
#     redis: Redis = Depends(get_redis),
# ) -> User:

#     # check blacklist

#     blacklisted = await is_token_blacklisted(
#         redis,
#         token
#     )

#     if blacklisted:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token revoked"
#         )

#     # decode token

#     payload = verify_access_token(token)

#     user_id = get_user_id_from_payload(payload)

#     if not user_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token"
#         )

#     # fetch user

#     result = await db.execute(
#         select(User).where(
#             User.id == int(user_id)
#         )
#     )

#     user = result.scalar_one_or_none()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found"
#         )

#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Account disabled"
#         )

#     return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):

    print("=" * 50)
    print("TOKEN FROM DEPENDENCY:", token)

    # blacklisted = await is_token_blacklisted(redis, token)

    # print("BLACKLISTED:", blacklisted)

    # payload = verify_access_token(token)

    # print("PAYLOAD:", payload)

    # user_id = get_user_id_from_payload(payload)

    # print("USER_ID:", user_id)

    # result = await db.execute(
    #     select(User).where(User.id == int(user_id))
    # )

    # user = result.scalar_one_or_none()

    # print("USER:", user)

    # return user

    # Skip Redis blacklist during testing
    blacklisted = False

    payload = verify_access_token(token)

    user_id = get_user_id_from_payload(payload)

    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# =====================================================
# VERIFIED USER
# =====================================================

async def get_verified_user(
    current_user: User = Depends(
        get_current_user
    )
) -> User:

    if not current_user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified"
        )

    return current_user


# =====================================================
# ADMIN USER
# =====================================================

async def get_admin_user(
    current_user: User = Depends(
        get_verified_user
    )
) -> User:

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user


# =====================================================
# CUSTOMER USER
# =====================================================

async def get_customer_user(
    current_user: User = Depends(
        get_verified_user
    )
) -> User:

    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer access required"
        )

    return current_user








# from fastapi import Depends, HTTPException, status
# from jose import jwt, JWTError
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.core.config import settings
# from app.core.database import get_db
# from app.models import User

# async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
    
#     user = await db.execute(select(User).where(User.username == username))
#     user = user.scalar_one_or_none()
#     if user is None:
#         raise credentials_exception
#     return user






# --------------------------------------------------------------------------------

# from typing import Annotated

# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from redis.asyncio import Redis

# from app.core.database import get_db
# from app.core.security import (
#     verify_access_token,
#     is_token_blacklisted,
#     get_user_id_from_payload,
# )
# from app.models.user import User
# from app.models.user import UserRole
# from app.db.redis import get_redis




# from typing import Optional, List, Callable

# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.ext.asyncio import AsyncSession
# from jose import JWTError, jwt

# from app.db.session import get_db
# from app.services.user_service import user_service
# from app.core.config import settings
# from app.models.user import User


# # =====================================================
# # OAUTH2 SCHEME
# # =====================================================

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# # =====================================================
# # DECODE TOKEN
# # =====================================================

# def decode_access_token(token: str) -> dict:
#     try:
#         payload = jwt.decode(
#             token,
#             settings.SECRET_KEY,
#             algorithms=[settings.ALGORITHM],
#         )
#         return payload

#     except JWTError:
#         return {}


# # =====================================================
# # GET CURRENT USER (CORE DEPENDENCY)
# # =====================================================

# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: AsyncSession = Depends(get_db),
# ) -> User:

#     payload = decode_access_token(token)

#     if not payload:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication token",
#         )

#     user_id = payload.get("sub")

#     if not user_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token payload",
#         )

#     user = await user_service.get_user(db, int(user_id))

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found",
#         )

#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="User account disabled",
#         )

#     return user


# # =====================================================
# # OPTIONAL USER (FOR PUBLIC ROUTES)
# # =====================================================

# async def get_optional_user(
#     token: Optional[str] = Depends(oauth2_scheme),
#     db: AsyncSession = Depends(get_db),
# ) -> Optional[User]:

#     if not token:
#         return None

#     payload = decode_access_token(token)

#     if not payload:
#         return None

#     user_id = payload.get("sub")

#     if not user_id:
#         return None

#     return await user_service.get_user(db, int(user_id))


# # =====================================================
# # ROLE CHECKER FACTORY (RBAC)
# # =====================================================

# def require_roles(allowed_roles: List[str]) -> Callable:

#     async def role_checker(
#         user: User = Depends(get_current_user),
#     ) -> User:

#         if user.role not in allowed_roles:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Insufficient permissions",
#             )

#         return user

#     return role_checker


# # =====================================================
# # PREDEFINED ROLE DEPENDENCIES
# # =====================================================

# require_admin = require_roles(["admin"])
# require_customer = require_roles(["customer", "admin"])


# # =====================================================
# # ADMIN ONLY (STRICT GUARD)
# # =====================================================

# async def admin_only(
#     user: User = Depends(get_current_user),
# ) -> User:

#     if user.role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Admin access required",
#         )

#     return user
# # ==========================================================
# # OAUTH2
# # ==========================================================

# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="/api/auth/login"
# )


# # ==========================================================
# # DATABASE DEPENDENCY
# # ==========================================================

# DBSession = Annotated[
#     AsyncSession,
#     Depends(get_db)
# ]


# # ==========================================================
# # REDIS DEPENDENCY
# # ==========================================================

# RedisSession = Annotated[
#     Redis,
#     Depends(get_redis)
# ]


# # ==========================================================
# # CURRENT USER
# # ==========================================================

# async def get_current_user(
#     token: Annotated[
#         str,
#         Depends(oauth2_scheme)
#     ],
#     db: DBSession,
#     redis: RedisSession,
# ) -> User:

#     # -----------------------------
#     # blacklist check
#     # -----------------------------

#     blacklisted = await is_token_blacklisted(
#         redis,
#         token,
#     )

#     if blacklisted:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token revoked",
#         )

#     # -----------------------------
#     # verify token
#     # -----------------------------

#     payload = verify_access_token(
#         token
#     )

#     user_id = get_user_id_from_payload(
#         payload
#     )

#     # -----------------------------
#     # fetch user
#     # -----------------------------

#     stmt = (
#         select(User)
#         .where(User.id == user_id)
#     )

#     result = await db.execute(
#         stmt
#     )

#     user = result.scalar_one_or_none()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found",
#         )

#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Account disabled",
#         )

#     return user


# # ==========================================================
# # ACTIVE USER
# # ==========================================================

# async def get_current_active_user(
#     current_user: Annotated[
#         User,
#         Depends(get_current_user)
#     ]
# ) -> User:

#     if not current_user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Inactive account",
#         )

#     return current_user


# # ==========================================================
# # VERIFIED EMAIL USER
# # ==========================================================

# async def get_verified_user(
#     current_user: Annotated[
#         User,
#         Depends(get_current_active_user)
#     ]
# ) -> User:

#     if not current_user.is_email_verified:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Email not verified",
#         )

#     return current_user


# # ==========================================================
# # ADMIN USER
# # ==========================================================

# async def get_admin_user(
#     current_user: Annotated[
#         User,
#         Depends(get_verified_user)
#     ]
# ) -> User:

#     if current_user.role != UserRole.ADMIN:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Admin access required",
#         )

#     return current_user


# # ==========================================================
# # CUSTOMER USER
# # ==========================================================

# async def get_customer_user(
#     current_user: Annotated[
#         User,
#         Depends(get_verified_user)
#     ]
# ) -> User:

#     if current_user.role != UserRole.CUSTOMER:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Customer access required",
#         )

#     return current_user


# # ==========================================================
# # ROLE BASED DEPENDENCY
# # ==========================================================

# class RoleChecker:

#     def __init__(
#         self,
#         allowed_roles: list[str]
#     ):
#         self.allowed_roles = allowed_roles

#     async def __call__(
#         self,
#         current_user: Annotated[
#             User,
#             Depends(get_verified_user)
#         ]
#     ):

#         if (
#             current_user.role
#             not in self.allowed_roles
#         ):
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Permission denied",
#             )

#         return current_user


# # ==========================================================
# # COMMON ROLE CHECKERS
# # ==========================================================

# AdminOnly = RoleChecker(
#     [UserRole.ADMIN]
# )

# CustomerOnly = RoleChecker(
#     [UserRole.CUSTOMER]
# )

# AdminOrCustomer = RoleChecker(
#     [
#         UserRole.ADMIN,
#         UserRole.CUSTOMER,
#     ]
# )


# # ==========================================================
# # PAGINATION
# # ==========================================================

# def pagination_params(
#     page: int = 1,
#     page_size: int = 20,
# ):

#     if page < 1:
#         page = 1

#     if page_size < 1:
#         page_size = 20

#     if page_size > 100:
#         page_size = 100

#     return {
#         "page": page,
#         "page_size": page_size,
#         "offset": (
#             (page - 1)
#             * page_size
#         ),
#     }


# # ==========================================================
# # SORTING
# # ==========================================================

# def sorting_params(
#     sort_by: str = "id",
#     order: str = "desc",
# ):

#     return {
#         "sort_by": sort_by,
#         "order": order.lower(),
#     }


# # ==========================================================
# # SEARCH
# # ==========================================================

# def search_params(
#     search: str | None = None
# ):

#     return {
#         "search": search
#     }


# # ==========================================================
# # COMMON DEPENDENCY ALIASES
# # ==========================================================

# CurrentUser = Annotated[
#     User,
#     Depends(get_current_user)
# ]

# ActiveUser = Annotated[
#     User,
#     Depends(get_current_active_user)
# ]

# VerifiedUser = Annotated[
#     User,
#     Depends(get_verified_user)
# ]

# AdminUser = Annotated[
#     User,
#     Depends(get_admin_user)
# ]

# CustomerUser = Annotated[
#     User,
#     Depends(get_customer_user)
# ]




