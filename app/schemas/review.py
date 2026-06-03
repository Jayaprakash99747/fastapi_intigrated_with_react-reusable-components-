from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


# ==========================================================
# CREATE REVIEW
# ==========================================================

class ReviewCreate(BaseModel):

    product_id: int = Field(
        ...,
        gt=0,
    )

    rating: int = Field(
        ...,
        ge=1,
        le=5,
    )

    comment: Optional[str] = Field(
        default=None,
        max_length=2000,
    )


# ==========================================================
# UPDATE REVIEW
# ==========================================================

class ReviewUpdate(BaseModel):

    rating: Optional[int] = Field(
        default=None,
        ge=1,
        le=5,
    )

    comment: Optional[str] = Field(
        default=None,
        max_length=2000,
    )


# ==========================================================
# REVIEW USER
# ==========================================================

class ReviewUserResponse(BaseModel):

    id: int

    username: str

    profile_image: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# REVIEW PRODUCT
# ==========================================================

class ReviewProductResponse(BaseModel):

    id: int

    name: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# REVIEW RESPONSE
# ==========================================================

class ReviewResponse(BaseModel):

    id: int

    product_id: int

    user_id: int

    rating: int

    comment: Optional[str]

    is_verified_purchase: bool

    created_at: datetime

    updated_at: datetime

    user: Optional[
        ReviewUserResponse
    ] = None

    product: Optional[
        ReviewProductResponse
    ] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# REVIEW LIST ITEM
# ==========================================================

class ReviewListItem(BaseModel):

    id: int

    rating: int

    comment: Optional[str]

    is_verified_purchase: bool

    created_at: datetime

    user: Optional[
        ReviewUserResponse
    ] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# REVIEW LIST RESPONSE
# ==========================================================

class ReviewListResponse(BaseModel):

    items: list[
        ReviewListItem
    ]


# ==========================================================
# PRODUCT REVIEWS RESPONSE
# ==========================================================

class ProductReviewsResponse(BaseModel):

    product_id: int

    average_rating: float

    total_reviews: int

    items: list[
        ReviewListItem
    ]


# ==========================================================
# REVIEW STATS
# ==========================================================

class ReviewStatsResponse(BaseModel):

    product_id: int

    average_rating: float

    total_reviews: int

    rating_1_count: int

    rating_2_count: int

    rating_3_count: int

    rating_4_count: int

    rating_5_count: int


# ==========================================================
# REVIEW DELETE RESPONSE
# ==========================================================

class ReviewDeleteResponse(BaseModel):

    message: str


# ==========================================================
# REVIEW MESSAGE RESPONSE
# ==========================================================

class ReviewMessageResponse(BaseModel):

    message: str