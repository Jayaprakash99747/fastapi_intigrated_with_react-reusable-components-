from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.constants import UserRole


# ==========================================================
# USER
# ==========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True,)

    username = Column(String(100),unique=True,nullable=False,index=True,)

    email = Column(String(255),unique=True,nullable=False,index=True,)

    password = Column(String(255),nullable=False,)

    role = Column(Enum(UserRole),nullable=False,default=UserRole.CUSTOMER,)

    phone = Column(String(20),nullable=True,)

    address = Column(Text,nullable=True,)

    city = Column(String(100),nullable=True,)

    state = Column(String(100),nullable=True,)

    pincode = Column(String(20),nullable=True,)

    profile_image = Column(String(500),nullable=True,)

    is_active = Column(Boolean,default=True,nullable=False,)

    is_email_verified = Column(Boolean,default=False,nullable=False,)

    last_login = Column(DateTime,nullable=True,)

    created_at = Column(DateTime,default=datetime.utcnow,nullable=False,)

    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False,)

    # ======================================================
    # RELATIONSHIPS
    # ======================================================

    refresh_tokens = relationship("RefreshToken",back_populates="user",cascade="all, delete-orphan",passive_deletes=True,)

    reset_codes = relationship("PasswordResetCode",back_populates="user",cascade="all, delete-orphan",passive_deletes=True,)

    cart_items = relationship("CartItem",back_populates="user",cascade="all, delete-orphan",passive_deletes=True,)

    wishlist_items = relationship("WishlistItem",back_populates="user",cascade="all, delete-orphan",passive_deletes=True,)

    orders = relationship("Order",back_populates="user",)

    reviews = relationship("Review",back_populates="user",)

    def __repr__(self):
        return (
            f"<User("
            f"id={self.id}, "
            f"email='{self.email}', "
            f"role='{self.role}'"
            f")>"
        )


# ==========================================================
# REFRESH TOKEN
# ==========================================================

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer,primary_key=True,index=True,)

    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE",),nullable=False,index=True,)

    token = Column(String(1000),nullable=False,unique=True,index=True,)

    expires_at = Column(DateTime,nullable=False,)

    is_revoked = Column(Boolean,default=False,nullable=False,)

    created_at = Column(DateTime,default=datetime.utcnow,nullable=False,)

    user = relationship("User",back_populates="refresh_tokens",)

    def __repr__(self):
        return (
            f"<RefreshToken("
            f"id={self.id}, "
            f"user_id={self.user_id}"
            f")>"
        )


# ==========================================================
# PASSWORD RESET CODE
# ==========================================================

class PasswordResetCode(Base):
    __tablename__ = "password_reset_codes"

    id = Column(Integer,primary_key=True,index=True,)

    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE",),nullable=False,index=True,)

    reset_code = Column(String(20),nullable=False,index=True,)

    expires_at = Column(DateTime,nullable=False,)

    is_used = Column(Boolean,default=False,nullable=False,)

    created_at = Column(DateTime,default=datetime.utcnow,nullable=False,)

    user = relationship("User",back_populates="reset_codes",)

    def __repr__(self):
        return (
            f"<PasswordResetCode("
            f"id={self.id}, "
            f"user_id={self.user_id}"
            f")>"
        )