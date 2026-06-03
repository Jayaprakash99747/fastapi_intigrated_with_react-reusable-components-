from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


# ==========================================================
# PRODUCT IMAGE
# ==========================================================

class ProductImageCreate(BaseModel):

    image_url: str = Field(
        ...,
        max_length=1000,
    )

    is_primary: bool = False


class ProductImageResponse(BaseModel):

    id: int

    image_url: str

    is_primary: bool

    model_config = ConfigDict(
        from_attributes=True
    )

# ==========================================================
# CATEGORY RESPONSE
# ==========================================================

class CategoryMiniResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )

# ==========================================================
# PRODUCT BASE
# ==========================================================

class ProductBase(BaseModel):

    category_id: int

    name: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    description: Optional[str] = None

    brand: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    sku: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    price: float = Field(
        ...,
        gt=0,
    )

    discount_percent: float = Field(
        default=0,
        ge=0,
        le=100,
    )

    gst_percent: float = Field(
        default=18,
        ge=0,
        le=100,
    )

    stock_quantity: int = Field(
        default=0,
        ge=0,
    )

    is_available: bool = True

    is_featured: bool = False


# ==========================================================
# CREATE
# ==========================================================

class ProductCreate(ProductBase):

    images: list[ProductImageCreate] = []


# ==========================================================
# UPDATE
# ==========================================================

class ProductUpdate(BaseModel):

    category_id: Optional[int] = None

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    description: Optional[str] = None

    brand: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    sku: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    price: Optional[float] = Field(
        default=None,
        gt=0,
    )

    discount_percent: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
    )

    gst_percent: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
    )

    stock_quantity: Optional[int] = Field(
        default=None,
        ge=0,
    )

    is_available: Optional[bool] = None

    is_featured: Optional[bool] = None


# ==========================================================
# CATEGORY INFO
# ==========================================================

class ProductCategoryResponse(BaseModel):

    id: int

    name: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# PRODUCT RESPONSE
# ==========================================================

class ProductResponse(BaseModel):

    id: int

    category_id: int

    name: str

    description: Optional[str]

    brand: Optional[str]

    sku: Optional[str]

    price: float

    discount_percent: float

    gst_percent: float

    rating: float

    stock_quantity: int

    is_available: bool

    is_featured: bool

    is_deleted: bool

    created_at: datetime

    updated_at: datetime

    category: Optional[
        ProductCategoryResponse
    ] = None

    images: list[
        ProductImageResponse
    ] = []

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# PRODUCT DETAIL
# ==========================================================

class ProductDetailResponse(ProductResponse):

    final_price: float = 0

    review_count: int = 0

    available_stock: int = 0


# ==========================================================
# PRODUCT LIST ITEM
# ==========================================================

class ProductListItem(BaseModel):

    id: int

    name: str

    brand: Optional[str]

    price: float

    rating: float

    stock_quantity: int

    is_available: bool

    is_featured: bool

    thumbnail: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# PRODUCT LIST RESPONSE
# ==========================================================

class ProductListResponse(BaseModel):

    items: list[
        ProductListItem
    ]


# ==========================================================
# FEATURED PRODUCTS
# ==========================================================

class FeaturedProductResponse(BaseModel):

    items: list[
        ProductListItem
    ]


# ==========================================================
# PAGINATION
# ==========================================================

class PaginatedProductResponse(BaseModel):

    total: int

    page: int

    page_size: int

    total_pages: int

    items: list[
        ProductListItem
    ]


# ==========================================================
# SEARCH
# ==========================================================

class ProductSearchRequest(BaseModel):

    keyword: Optional[str] = None

    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
    )


# ==========================================================
# FILTER
# ==========================================================

class ProductFilterRequest(BaseModel):

    category_id: Optional[int] = None

    brand: Optional[str] = None

    min_price: Optional[float] = None

    max_price: Optional[float] = None

    is_featured: Optional[bool] = None

    is_available: Optional[bool] = None

    min_rating: Optional[float] = None

    sort_by: Optional[str] = "created_at"

    sort_order: Optional[str] = "desc"

    page: int = 1

    page_size: int = 10


# ==========================================================
# PRODUCT DELETE RESPONSE
# ==========================================================

class ProductDeleteResponse(BaseModel):

    message: str


# ==========================================================
# PRODUCT STATS
# ==========================================================

class ProductStatsResponse(BaseModel):

    total_products: int

    active_products: int

    featured_products: int

    out_of_stock_products: int


# ==========================================================
# PRODUCT MESSAGE
# ==========================================================

class ProductMessageResponse(BaseModel):

    message: str
