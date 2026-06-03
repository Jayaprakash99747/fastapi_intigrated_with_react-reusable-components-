from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict,
    field_validator,
)

import re

from app.core.constants import UserRole


# ==========================================================
# BASE USER
# ==========================================================

class UserBase(BaseModel):

    username: str = Field(
        ...,
        min_length=3,
        max_length=100,
    )

    email: EmailStr

    phone: Optional[str] = Field(
        default=None,
        max_length=20,
    )

    address: Optional[str] = None

    city: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    state: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    pincode: Optional[str] = Field(
        default=None,
        max_length=20,
    )

    profile_image: Optional[str] = None


# ==========================================================
# USER CREATE
# ==========================================================

class UserCreate(UserBase):

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    @field_validator("password")
    @classmethod
    def validate_password(
        cls,
        value: str,
    ):

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain uppercase letter"
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain lowercase letter"
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain number"
            )

        if not re.search(
            r"[!@#$%^&*(),.?\":{}|<>]",
            value,
        ):
            raise ValueError(
                "Password must contain special character"
            )

        return value


# ==========================================================
# USER UPDATE
# ==========================================================

class UserUpdateSchema(BaseModel):

    username: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
    )

    phone: Optional[str] = Field(
        default=None,
        max_length=20,
    )

    address: Optional[str] = None

    city: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    state: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    pincode: Optional[str] = Field(
        default=None,
        max_length=20,
    )

    profile_image: Optional[str] = None


# ==========================================================
# USER RESPONSE
# ==========================================================

class UserResponse(BaseModel):

    id: int

    username: str

    email: EmailStr

    role: UserRole

    phone: Optional[str]

    address: Optional[str]

    city: Optional[str]

    state: Optional[str]

    pincode: Optional[str]

    profile_image: Optional[str]

    is_active: bool

    is_email_verified: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# USER PROFILE RESPONSE
# ==========================================================

class UserProfileResponse(UserResponse):

    last_login: Optional[datetime] = None


# ==========================================================
# CHANGE PASSWORD
# ==========================================================

class PasswordChangeSchema(BaseModel):

    current_password: str

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    @field_validator("new_password")
    @classmethod
    def validate_password(
        cls,
        value: str,
    ):

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain uppercase letter"
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain lowercase letter"
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain number"
            )

        if not re.search(
            r"[!@#$%^&*(),.?\":{}|<>]",
            value,
        ):
            raise ValueError(
                "Password must contain special character"
            )

        return value


# ==========================================================
# DELETE ACCOUNT
# ==========================================================

class DeleteAccountRequest(BaseModel):

    password: str


# ==========================================================
# ADMIN USER RESPONSE
# ==========================================================

class AdminUserResponse(UserResponse):

    last_login: Optional[datetime]

    refresh_token_count: Optional[int] = 0


# ==========================================================
# USER LIST ITEM
# ==========================================================

class UserListItem(BaseModel):

    id: int

    username: str

    email: EmailStr

    role: UserRole

    is_active: bool

    is_email_verified: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# PAGINATED USERS RESPONSE
# ==========================================================

class PaginatedUsersResponse(BaseModel):

    total: int

    page: int

    page_size: int

    items: list[UserListItem]


# ==========================================================
# USER STATS RESPONSE
# ==========================================================

class UserStatsResponse(BaseModel):

    total_users: int

    active_users: int

    inactive_users: int

    verified_users: int

    admin_users: int

    customer_users: int


# ==========================================================
# USER STATUS UPDATE
# ==========================================================

class UserStatusUpdateRequest(BaseModel):

    is_active: bool


# ==========================================================
# USER ROLE UPDATE
# ==========================================================

class UserRoleUpdateRequest(BaseModel):

    role: UserRole


# ==========================================================
# SIMPLE MESSAGE
# ==========================================================

class UserMessageResponse(BaseModel):

    message: str


# ==========================================================
# Email Update
# ==========================================================

class EmailUpdateSchema(BaseModel):
    email: EmailStr