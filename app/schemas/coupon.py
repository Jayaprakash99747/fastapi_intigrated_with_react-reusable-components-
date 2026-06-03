from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


# ==========================================================
# COUPON CREATE
# ==========================================================

class CouponCreate(BaseModel):

    code: str = Field(
        ...,
        min_length=3,
        max_length=50,
    )

    discount_percent: float = Field(
        ...,
        gt=0,
        le=100,
    )

    max_uses: int = Field(
        default=100,
        ge=1,
    )

    min_order_amount: float = Field(
        default=0,
        ge=0,
    )

    expiry_date: datetime


# ==========================================================
# COUPON UPDATE
# ==========================================================

class CouponUpdate(BaseModel):

    discount_percent: Optional[float] = Field(
        default=None,
        gt=0,
        le=100,
    )

    max_uses: Optional[int] = Field(
        default=None,
        ge=1,
    )

    min_order_amount: Optional[float] = Field(
        default=None,
        ge=0,
    )

    is_active: Optional[bool] = None

    expiry_date: Optional[datetime] = None


# ==========================================================
# APPLY COUPON
# ==========================================================

class CouponApplyRequest(BaseModel):

    code: str = Field(
        ...,
        min_length=3,
        max_length=50,
    )

    order_amount: float = Field(
        ...,
        gt=0,
    )


# ==========================================================
# COUPON RESPONSE
# ==========================================================

class CouponResponse(BaseModel):

    id: int

    code: str

    discount_percent: float

    max_uses: int

    current_uses: int

    min_order_amount: float

    is_active: bool

    expiry_date: datetime

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# COUPON LIST ITEM
# ==========================================================

class CouponListItem(BaseModel):

    id: int

    code: str

    discount_percent: float

    current_uses: int

    max_uses: int

    is_active: bool

    expiry_date: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# COUPON LIST RESPONSE
# ==========================================================

class CouponListResponse(BaseModel):

    items: list[CouponListItem]


# ==========================================================
# COUPON VALIDATION RESPONSE
# ==========================================================

class CouponValidationResponse(BaseModel):

    valid: bool

    code: str

    discount_percent: float = 0

    discount_amount: float = 0

    final_amount: float = 0

    message: str


# ==========================================================
# COUPON APPLY RESPONSE
# ==========================================================

class CouponApplyResponse(BaseModel):

    coupon_id: int

    code: str

    order_amount: float

    discount_percent: float

    discount_amount: float

    final_amount: float


# ==========================================================
# COUPON STATS
# ==========================================================

class CouponStatsResponse(BaseModel):

    total_coupons: int

    active_coupons: int

    expired_coupons: int

    used_coupons: int


# ==========================================================
# COUPON DELETE RESPONSE
# ==========================================================

class CouponDeleteResponse(BaseModel):

    message: str


# ==========================================================
# GENERIC RESPONSE
# ==========================================================

class CouponMessageResponse(BaseModel):

    message: str