from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    HttpUrl,
)


# ==========================================================
# BANNER CREATE
# ==========================================================

class BannerCreate(BaseModel):

    title: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
    )

    image_url: HttpUrl

    button_text: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    button_link: Optional[HttpUrl] = None

    is_active: bool = True

    display_order: int = Field(
        default=0,
        ge=0,
    )


# ==========================================================
# BANNER UPDATE
# ==========================================================

class BannerUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
    )

    image_url: Optional[HttpUrl] = None

    button_text: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    button_link: Optional[HttpUrl] = None

    is_active: Optional[bool] = None

    display_order: Optional[int] = Field(
        default=None,
        ge=0,
    )


# ==========================================================
# BANNER RESPONSE
# ==========================================================

class BannerResponse(BaseModel):

    id: int

    title: str

    description: Optional[str]

    image_url: str

    button_text: Optional[str]

    button_link: Optional[str]

    is_active: bool

    display_order: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# BANNER LIST ITEM
# ==========================================================

class BannerListItem(BaseModel):

    id: int

    title: str

    image_url: str

    button_text: Optional[str]

    button_link: Optional[str]

    display_order: int

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# BANNER LIST RESPONSE
# ==========================================================

class BannerListResponse(BaseModel):

    items: list[BannerListItem]


# ==========================================================
# ACTIVE BANNERS RESPONSE
# ==========================================================

class ActiveBannerResponse(BaseModel):

    items: list[BannerListItem]


# ==========================================================
# BANNER STATS
# ==========================================================

class BannerStatsResponse(BaseModel):

    total_banners: int

    active_banners: int

    inactive_banners: int


# ==========================================================
# BANNER DELETE RESPONSE
# ==========================================================

class BannerDeleteResponse(BaseModel):

    message: str


# ==========================================================
# BANNER MESSAGE RESPONSE
# ==========================================================

class BannerMessageResponse(BaseModel):

    message: str