from fastapi import (
    APIRouter,
    File,
    Form,
    UploadFile,
    Depends,
    HTTPException,
    Query,
    status,
)
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.curd.banner import hero_crud

from app.schemas.banner import (
    HeroCreate,
    HeroUpdate,
    HeroResponse,
    HeroListResponse,
    APIResponse,
)
from app.models.banner import HeroSection
from app.services.file_service import FileService
from sqlalchemy import update, select



router = APIRouter(
    prefix="/hero",
    tags=["Hero Section"]
)


# ==========================================================
# CREATE HERO
# ==========================================================

@router.post(
    "/",
    response_model=HeroResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_hero(
    title: str = Form(...),
    description: str = Form(...),

    primary_button_text: str | None = Form(None),
    primary_button_url: str | None = Form(None),

    secondary_button_text: str | None = Form(None),
    secondary_button_url: str | None = Form(None),

    card_title: str | None = Form(None),
    card_description: str | None = Form(None),

    background_image: UploadFile | None = File(None),
    hero_image: UploadFile | None = File(None),

    is_active: bool = Form(True),
    display_order: int = Form(0),

    db: AsyncSession = Depends(get_db),
):
    background_path = None
    hero_path = None

    if background_image:
        background_path = await FileService.save_image(
            background_image
        )

    if hero_image:
        hero_path = await FileService.save_image(
            hero_image
        )

    payload = HeroCreate(
        title=title,
        description=description,

        primary_button_text=primary_button_text,
        primary_button_url=primary_button_url,

        secondary_button_text=secondary_button_text,
        secondary_button_url=secondary_button_url,

        card_title=card_title,
        card_description=card_description,

        background_image=background_path,
        hero_image=hero_path,

        is_active=is_active,
        display_order=display_order,
    )

    return await hero_crud.create(
        db=db,
        payload=payload,
    )


# ==========================================================
# GET ACTIVE HERO
# ==========================================================

@router.get(
    "/active",
    response_model=HeroResponse,
    status_code=status.HTTP_200_OK,
)
async def get_active_hero(
    db: AsyncSession = Depends(get_db),
):
    hero = await hero_crud.get_active(db)

    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active hero section not found",
        )

    return hero


# ==========================================================
# GET ALL HEROES
# ==========================================================

@router.get(
    "/",
    response_model=HeroListResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_heroes(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: AsyncSession = Depends(get_db),
):
    total, heroes = await hero_crud.get_all(
        db=db,
        skip=skip,
        limit=limit,
    )

    return HeroListResponse(
        total=total,
        items=heroes,
    )


# ==========================================================
# GET HERO BY ID
# ==========================================================

@router.get(
    "/{hero_id}",
    response_model=HeroResponse,
    status_code=status.HTTP_200_OK,
)
async def get_hero_by_id(
    hero_id: int,
    db: AsyncSession = Depends(get_db),
):
    hero = await hero_crud.get_by_id(
        db,
        hero_id,
    )

    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero section not found",
        )

    return hero


# ==========================================================
# UPDATE HERO
# ==========================================================

# @router.put(
#     "/{hero_id}",
#     response_model=HeroResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def update_hero(
#     hero_id: int,
#     payload: HeroUpdate,
#     db: AsyncSession = Depends(get_db),
# ):
#     hero = await hero_crud.get_by_id(
#         db,
#         hero_id,
#     )

#     if not hero:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Hero section not found",
#         )

#     return await hero_crud.update(
#         db=db,
#         hero=hero,
#         payload=payload,
#     )


# banners.py router



@router.put(
    "/{hero_id}",
    response_model=HeroResponse,
    status_code=status.HTTP_200_OK,
)
async def update_hero(
    hero_id: int,
    # ✅ Every field from HeroUpdate as Form(...) or Form(None)
    title:                  Optional[str]  = Form(None),
    description:            Optional[str]  = Form(None),
    primary_button_text:    Optional[str]  = Form(None),
    primary_button_url:     Optional[str]  = Form(None),
    secondary_button_text:  Optional[str]  = Form(None),
    secondary_button_url:   Optional[str]  = Form(None),
    card_title:             Optional[str]  = Form(None),
    card_description:       Optional[str]  = Form(None),
    is_active:              Optional[int]  = Form(None),   # ✅ int because FormData sends 1/0
    display_order:          Optional[int]  = Form(None),
    background_image:       Optional[UploadFile] = File(None),
    hero_image:             Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):
    hero = await hero_crud.get_by_id(db, hero_id)

    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero section not found",
        )

    # Build HeroUpdate from the form fields manually
    payload = HeroUpdate(
        title=title,
        description=description,
        primary_button_text=primary_button_text,
        primary_button_url=primary_button_url,
        secondary_button_text=secondary_button_text,
        secondary_button_url=secondary_button_url,
        card_title=card_title,
        card_description=card_description,
        is_active=bool(is_active) if is_active is not None else None,  # ✅ 1/0 → True/False
        display_order=display_order,
    )

    return await hero_crud.update(
        db=db,
        hero=hero,
        payload=payload,
        background_image=background_image,
        hero_image=hero_image,
    )

# ==========================================================
# SOFT DELETE HERO
# ==========================================================

@router.delete(
    "/{hero_id}",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_hero(
    hero_id: int,
    db: AsyncSession = Depends(get_db),
):
    hero = await hero_crud.get_by_id(
        db,
        hero_id,
    )

    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero section not found",
        )

    await hero_crud.delete(
        db,
        hero,
    )

    return APIResponse(
        success=True,
        message="Hero section deleted successfully",
    )


# ==========================================================
# RESTORE HERO
# ==========================================================

@router.post(
    "/{hero_id}/restore",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
)
async def restore_hero(
    hero_id: int,
    db: AsyncSession = Depends(get_db),
):
    hero = await hero_crud.restore(
        db,
        hero_id,
    )

    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deleted hero section not found",
        )

    return APIResponse(
        success=True,
        message="Hero section restored successfully",
    )


# ==========================================================
# PERMANENT DELETE
# ==========================================================

@router.delete(
    "/{hero_id}/hard-delete",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
)
async def hard_delete_hero(
    hero_id: int,
    db: AsyncSession = Depends(get_db),
):
    deleted = await hero_crud.hard_delete(
        db,
        hero_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero section not found",
        )

    return APIResponse(
        success=True,
        message="Hero section permanently deleted",
    )

# --------------------------------------------
# change banner from the admin list page
# --------------------------------------------




@router.patch("/{hero_id}/activate", response_model=APIResponse)
async def activate_hero(hero_id: int, db: AsyncSession = Depends(get_db)):
    # Check if hero exists
    hero = await db.get(HeroSection, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    # Deactivate all heroes
    await db.execute(
        update(HeroSection)
        .where(HeroSection.is_active == True)
        .values(is_active=False)
    )

    # Activate selected hero
    await db.execute(
        update(HeroSection)
        .where(HeroSection.id == hero_id)
        .values(is_active=True)
    )

    await db.commit()

    return APIResponse(
        success=True,
        message="Hero banner activated successfully"
    )