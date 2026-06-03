from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


# ==========================================================
# ADD TO CART
# ==========================================================

class CartItemCreate(BaseModel):

    product_id: int = Field(
        ...,
        gt=0,
    )

    quantity: int = Field(
        default=1,
        ge=1,
    )


# ==========================================================
# UPDATE CART ITEM
# ==========================================================

class CartItemUpdate(BaseModel):

    quantity: int = Field(
        ...,
        ge=1,
    )


# ==========================================================
# PRODUCT SUMMARY
# ==========================================================

class CartProductResponse(BaseModel):

    id: int

    name: str

    brand: Optional[str]

    price: float

    discount_percent: float

    stock_quantity: int

    is_available: bool

    thumbnail: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# CART ITEM RESPONSE
# ==========================================================

class CartItemResponse(BaseModel):

    id: int

    user_id: int

    product_id: int

    quantity: int

    created_at: datetime

    product: CartProductResponse

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# CART CALCULATION ITEM
# ==========================================================

class CartCalculationItem(BaseModel):

    cart_item_id: int

    product_id: int

    product_name: str

    quantity: int

    unit_price: float

    discount_percent: float

    subtotal: float

    discount_amount: float

    final_amount: float


# ==========================================================
# CART SUMMARY
# ==========================================================

class CartSummaryResponse(BaseModel):

    total_items: int

    subtotal: float

    total_discount: float

    gst_amount: float

    grand_total: float


# ==========================================================
# FULL CART RESPONSE
# ==========================================================

class CartResponse(BaseModel):

    items: list[CartItemResponse]

    summary: CartSummaryResponse


# ==========================================================
# CART LIST RESPONSE
# ==========================================================

class CartListResponse(BaseModel):

    items: list[CartItemResponse]


# ==========================================================
# CART COUNT RESPONSE
# ==========================================================

class CartCountResponse(BaseModel):

    total_items: int


# ==========================================================
# REMOVE CART ITEM RESPONSE
# ==========================================================

class RemoveCartItemResponse(BaseModel):

    message: str


# ==========================================================
# CLEAR CART RESPONSE
# ==========================================================

class ClearCartResponse(BaseModel):

    message: str


# ==========================================================
# CART VALIDATION RESPONSE
# ==========================================================

class CartValidationResponse(BaseModel):

    valid: bool

    message: str


# ==========================================================
# CART PRICE BREAKDOWN
# ==========================================================

class CartPriceBreakdown(BaseModel):

    subtotal: float

    discount_amount: float

    gst_amount: float

    shipping_amount: float

    grand_total: float


# ==========================================================
# CHECKOUT PREVIEW
# ==========================================================

class CheckoutPreviewResponse(BaseModel):

    cart_items: list[CartCalculationItem]

    pricing: CartPriceBreakdown


# ==========================================================
# GENERIC RESPONSE
# ==========================================================

class CartMessageResponse(BaseModel):

    message: str