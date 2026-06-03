from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)

from app.core.constants import OrderStatus


# ==========================================================
# CREATE ORDER
# ==========================================================

class OrderCreate(BaseModel):

    shipping_address: str = Field(
        ...,
        min_length=5,
        max_length=2000,
    )

    coupon_code: Optional[str] = None

    notes: Optional[str] = Field(
        default=None,
        max_length=1000,
    )


# ==========================================================
# ORDER ITEM CREATE
# ==========================================================

class OrderItemCreate(BaseModel):

    product_id: int = Field(
        ...,
        gt=0,
    )

    quantity: int = Field(
        ...,
        ge=1,
    )


# ==========================================================
# PRODUCT SNAPSHOT
# ==========================================================

class OrderProductResponse(BaseModel):

    id: int

    name: str

    brand: Optional[str]

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# ORDER ITEM RESPONSE
# ==========================================================

class OrderItemResponse(BaseModel):

    id: int

    product_id: int

    quantity: int

    unit_price: float

    discount_amount: float

    tax_amount: float

    product: Optional[
        OrderProductResponse
    ] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# ORDER RESPONSE
# ==========================================================

class OrderResponse(BaseModel):

    id: int

    user_id: int

    order_number: str

    status: OrderStatus

    total_amount: float

    tax_amount: float

    discount_amount: float

    shipping_address: str

    tracking_number: Optional[str]

    notes: Optional[str]

    created_at: datetime

    updated_at: datetime

    order_items: list[
        OrderItemResponse
    ] = []

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# ORDER DETAIL
# ==========================================================

class OrderDetailResponse(OrderResponse):

    item_count: int = 0


# ==========================================================
# ORDER LIST ITEM
# ==========================================================

class OrderListItem(BaseModel):

    id: int

    order_number: str

    status: OrderStatus

    total_amount: float

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# ORDER LIST RESPONSE
# ==========================================================

class OrderListResponse(BaseModel):

    items: list[
        OrderListItem
    ]


# ==========================================================
# PAGINATED ORDERS
# ==========================================================

class PaginatedOrderResponse(BaseModel):

    total: int

    page: int

    page_size: int

    total_pages: int

    items: list[
        OrderListItem
    ]


# ==========================================================
# CANCEL ORDER
# ==========================================================

class OrderCancelRequest(BaseModel):

    reason: Optional[str] = Field(
        default=None,
        max_length=500,
    )


# ==========================================================
# UPDATE STATUS (ADMIN)
# ==========================================================

class OrderStatusUpdate(BaseModel):

    status: OrderStatus

    tracking_number: Optional[str] = Field(
        default=None,
        max_length=200,
    )


# ==========================================================
# ORDER TRACKING
# ==========================================================

class OrderTrackingResponse(BaseModel):

    order_number: str

    status: OrderStatus

    tracking_number: Optional[str]

    updated_at: datetime


# ==========================================================
# ORDER SUMMARY
# ==========================================================

class OrderSummaryResponse(BaseModel):

    total_orders: int

    pending_orders: int

    confirmed_orders: int

    shipped_orders: int

    delivered_orders: int

    cancelled_orders: int


# ==========================================================
# DELETE RESPONSE
# ==========================================================

class OrderMessageResponse(BaseModel):

    message: str