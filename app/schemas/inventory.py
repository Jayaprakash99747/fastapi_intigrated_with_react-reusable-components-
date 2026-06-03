from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


# ==========================================================
# INVENTORY CREATE
# ==========================================================

class InventoryCreate(BaseModel):

    product_id: int = Field(
        ...,
        gt=0,
    )

    stock_in: int = Field(
        default=0,
        ge=0,
    )

    stock_out: int = Field(
        default=0,
        ge=0,
    )

    available_stock: int = Field(
        ...,
        ge=0,
    )

    reorder_level: int = Field(
        default=10,
        ge=0,
    )


# ==========================================================
# INVENTORY UPDATE
# ==========================================================

class InventoryUpdate(BaseModel):

    stock_in: Optional[int] = Field(
        default=None,
        ge=0,
    )

    stock_out: Optional[int] = Field(
        default=None,
        ge=0,
    )

    available_stock: Optional[int] = Field(
        default=None,
        ge=0,
    )

    reorder_level: Optional[int] = Field(
        default=None,
        ge=0,
    )


# ==========================================================
# STOCK IN
# ==========================================================

class StockInRequest(BaseModel):

    quantity: int = Field(
        ...,
        gt=0,
    )


# ==========================================================
# STOCK OUT
# ==========================================================

class StockOutRequest(BaseModel):

    quantity: int = Field(
        ...,
        gt=0,
    )


# ==========================================================
# PRODUCT INFO
# ==========================================================

class InventoryProductResponse(BaseModel):

    id: int

    name: str

    brand: Optional[str]

    stock_quantity: int

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# INVENTORY RESPONSE
# ==========================================================

class InventoryResponse(BaseModel):

    id: int

    product_id: int

    stock_in: int

    stock_out: int

    available_stock: int

    reorder_level: int

    last_updated: datetime

    created_at: datetime

    product: Optional[
        InventoryProductResponse
    ] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# INVENTORY DETAIL
# ==========================================================

class InventoryDetailResponse(
    InventoryResponse
):

    is_low_stock: bool = False

    is_out_of_stock: bool = False

    stock_percentage: float = 0


# ==========================================================
# INVENTORY LIST ITEM
# ==========================================================

class InventoryListItem(BaseModel):

    product_id: int

    available_stock: int

    reorder_level: int

    last_updated: datetime

    is_low_stock: bool

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# INVENTORY LIST RESPONSE
# ==========================================================

class InventoryListResponse(BaseModel):

    items: list[
        InventoryListItem
    ]


# ==========================================================
# LOW STOCK RESPONSE
# ==========================================================

class LowStockResponse(BaseModel):

    items: list[
        InventoryListItem
    ]


# ==========================================================
# INVENTORY STATS
# ==========================================================

class InventoryStatsResponse(BaseModel):

    total_products: int

    low_stock_products: int

    out_of_stock_products: int

    total_available_stock: int


# ==========================================================
# INVENTORY MESSAGE
# ==========================================================

class InventoryMessageResponse(BaseModel):

    message: str