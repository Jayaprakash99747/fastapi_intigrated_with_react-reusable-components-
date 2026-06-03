from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


# ==========================================================
# BASE CATEGORY
# ==========================================================

class CategoryBase(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Category name"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    image_url: Optional[str] = Field(
        default=None,
        max_length=1000,
    )


# ==========================================================
# CREATE
# ==========================================================

class CategoryCreate(CategoryBase):
    pass


# ==========================================================
# UPDATE
# ==========================================================

class CategoryUpdate(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    image_url: Optional[str] = Field(
        default=None,
        max_length=1000,
    )


# ==========================================================
# RESPONSE
# ==========================================================

class CategoryResponse(BaseModel):

    id: int

    name: str

    description: Optional[str]

    image_url: Optional[str]

    is_deleted: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# CATEGORY DETAIL
# ==========================================================

class CategoryDetailResponse(CategoryResponse):

    product_count: int = 0


# ==========================================================
# LIST ITEM
# ==========================================================

class CategoryListItem(BaseModel):

    id: int

    name: str

    image_url: Optional[str]

    product_count: int = 0

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# LIST RESPONSE
# ==========================================================

class CategoryListResponse(BaseModel):

    items: list[CategoryListItem]


# ==========================================================
# PAGINATION
# ==========================================================

class PaginatedCategoryResponse(BaseModel):

    total: int

    page: int

    page_size: int

    total_pages: int

    items: list[CategoryListItem]


# ==========================================================
# SEARCH
# ==========================================================

class CategorySearchRequest(BaseModel):

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
# DELETE RESPONSE
# ==========================================================

class CategoryDeleteResponse(BaseModel):

    message: str


# ==========================================================
# CATEGORY STATS
# ==========================================================

class CategoryStatsResponse(BaseModel):

    total_categories: int

    active_categories: int

    deleted_categories: int


# ==========================================================
# SIMPLE MESSAGE
# ==========================================================

class CategoryMessageResponse(BaseModel):

    message: str