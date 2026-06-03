from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


# ==========================================================
# ADD TO WISHLIST
# ==========================================================

class WishlistItemCreate(BaseModel):

    product_id: int = Field(
        ...,
        gt=0,
    )


# ==========================================================
# PRODUCT SUMMARY
# ==========================================================

class WishlistProductResponse(BaseModel):

    id: int

    name: str

    brand: Optional[str]

    price: float

    discount_percent: float

    rating: float

    stock_quantity: int

    is_available: bool

    is_featured: bool

    thumbnail: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# WISHLIST ITEM RESPONSE
# ==========================================================

class WishlistItemResponse(BaseModel):

    id: int

    user_id: int

    product_id: int

    created_at: datetime

    product: WishlistProductResponse

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# WISHLIST LIST RESPONSE
# ==========================================================

class WishlistResponse(BaseModel):

    items: list[WishlistItemResponse]


# ==========================================================
# WISHLIST COUNT RESPONSE
# ==========================================================

class WishlistCountResponse(BaseModel):

    total_items: int


# ==========================================================
# MOVE TO CART
# ==========================================================

class MoveWishlistToCartRequest(BaseModel):

    quantity: int = Field(
        default=1,
        ge=1,
    )


# ==========================================================
# DELETE RESPONSE
# ==========================================================

class WishlistDeleteResponse(BaseModel):

    message: str


# ==========================================================
# CLEAR RESPONSE
# ==========================================================

class WishlistClearResponse(BaseModel):

    message: str


# ==========================================================
# STATUS RESPONSE
# ==========================================================

class WishlistStatusResponse(BaseModel):

    exists: bool

    product_id: int


# ==========================================================
# GENERIC RESPONSE
# ==========================================================

class WishlistMessageResponse(BaseModel):

    message: str