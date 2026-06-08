from datetime import datetime
from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    ConfigDict,
)


# ==========================================================
# BASE SCHEMA (strict — input validation only)
# ==========================================================

class HeroBase(BaseModel):

    title: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Hero title"
    )

    description: str = Field(
        ...,
        min_length=10,
        description="Hero description"
    )

    primary_button_text: str | None = Field(
        default=None,
        max_length=100
    )

    primary_button_url: HttpUrl | None = None

    secondary_button_text: str | None = Field(
        default=None,
        max_length=100
    )

    secondary_button_url: HttpUrl | None = None

    card_title: str | None = Field(
        default=None,
        max_length=255
    )

    card_description: str | None = None

    background_image: str | None = None

    hero_image: str | None = None

    is_active: bool = True

    display_order: int = Field(
        default=0,
        ge=0
    )


# ==========================================================
# CREATE
# ==========================================================

class HeroCreate(HeroBase):
    pass


# ==========================================================
# UPDATE
# ==========================================================

class HeroUpdate(BaseModel):

    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=500
    )

    description: str | None = Field(
        default=None,
        min_length=10
    )

    primary_button_text: str | None = Field(
        default=None,
        max_length=100
    )

    primary_button_url: HttpUrl | None = None

    secondary_button_text: str | None = Field(
        default=None,
        max_length=100
    )

    secondary_button_url: HttpUrl | None = None

    card_title: str | None = Field(
        default=None,
        max_length=255
    )

    card_description: str | None = None

    background_image: str | None = None

    hero_image: str | None = None

    is_active: bool | None = None

    display_order: int | None = Field(
        default=None,
        ge=0
    )


# ==========================================================
# RESPONSE (lenient — DB data is already trusted)
# ✅ Does NOT inherit HeroBase — no strict validators
# ==========================================================

class HeroResponse(BaseModel):

    id: int

    # ✅ No min_length — old DB rows may have short values
    title: str

    # ✅ No min_length=10 — this was causing the 500
    description: str

    primary_button_text: str | None = None

    # ✅ Plain str, not HttpUrl — avoids URL parse errors on legacy data
    primary_button_url: str | None = None

    secondary_button_text: str | None = None

    # ✅ Plain str, not HttpUrl — same reason
    secondary_button_url: str | None = None

    card_title: str | None = None

    card_description: str | None = None

    background_image: str | None = None

    hero_image: str | None = None

    is_active: bool

    is_deleted: bool

    display_order: int

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# LIST RESPONSE
# ==========================================================

class HeroListResponse(BaseModel):

    total: int

    items: list[HeroResponse]


# ==========================================================
# COMMON API RESPONSE
# ==========================================================

class APIResponse(BaseModel):

    success: bool

    message: str


# ==========================================================
# DELETE RESPONSE
# ==========================================================

class HeroDeleteResponse(APIResponse):
    pass


# ==========================================================
# RESTORE RESPONSE
# ==========================================================

class HeroRestoreResponse(APIResponse):
    pass

















# from datetime import datetime
# from typing import Optional

# from pydantic import (
#     BaseModel,
#     Field,
#     ConfigDict,
#     HttpUrl,
# )


# # ==========================================================
# # BANNER CREATE
# # ==========================================================

# class BannerCreate(BaseModel):

#     title: str = Field(
#         ...,
#         min_length=2,
#         max_length=200,
#     )

#     description: Optional[str] = Field(
#         default=None,
#         max_length=2000,
#     )

#     image_url: HttpUrl

#     button_text: Optional[str] = Field(
#         default=None,
#         max_length=100,
#     )

#     button_link: Optional[HttpUrl] = None

#     is_active: bool = True

#     display_order: int = Field(
#         default=0,
#         ge=0,
#     )


# # ==========================================================
# # BANNER UPDATE
# # ==========================================================

# class BannerUpdate(BaseModel):

#     title: Optional[str] = Field(default=None,min_length=2,max_length=200,)

#     description: Optional[str] = Field(default=None,max_length=2000,)

#     image_url: Optional[HttpUrl] = None

#     button_text: Optional[str] = Field(default=None,max_length=100,)

#     button_link: Optional[HttpUrl] = None

#     is_active: Optional[bool] = None

#     display_order: Optional[int] = Field(default=None,ge=0,)


# # ==========================================================
# # BANNER RESPONSE
# # ==========================================================

# class BannerResponse(BaseModel):

#     id: int

#     title: str

#     description: Optional[str]

#     image_url: str

#     button_text: Optional[str]

#     button_link: Optional[str]

#     is_active: bool

#     display_order: int

#     created_at: datetime

#     model_config = ConfigDict(from_attributes=True)


# # ==========================================================
# # BANNER LIST ITEM
# # ==========================================================

# class BannerListItem(BaseModel):

#     id: int

#     title: str

#     image_url: str

#     button_text: Optional[str]

#     button_link: Optional[str]

#     display_order: int

#     is_active: bool

#     model_config = ConfigDict(from_attributes=True)


# # ==========================================================
# # BANNER LIST RESPONSE
# # ==========================================================

# class BannerListResponse(BaseModel):

#     items: list[BannerListItem]


# # ==========================================================
# # ACTIVE BANNERS RESPONSE
# # ==========================================================

# class ActiveBannerResponse(BaseModel):

#     items: list[BannerListItem]


# # ==========================================================
# # BANNER STATS
# # ==========================================================

# class BannerStatsResponse(BaseModel):

#     total_banners: int

#     active_banners: int

#     inactive_banners: int


# # ==========================================================
# # BANNER DELETE RESPONSE
# # ==========================================================

# class BannerDeleteResponse(BaseModel):

#     message: str


# # ==========================================================
# # BANNER MESSAGE RESPONSE
# # ==========================================================

# class BannerMessageResponse(BaseModel):

#     message: str