# app/crud/banner.py

import os
import uuid
from pathlib import Path
from datetime import datetime

from fastapi import UploadFile
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.banner import HeroSection
from app.schemas.banner import HeroCreate, HeroUpdate

# ── Module-level constants (outside the class) ────────────────────────────────
UPLOAD_DIR = Path("media/heroes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ── Module-level helper (outside the class) ───────────────────────────────────
async def save_upload(file: UploadFile) -> str:
    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4().hex}{ext}"
    path = UPLOAD_DIR / filename
    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)
    return f"/media/heroes/{filename}"


# ─────────────────────────────────────────────────────────────────────────────
class HeroCRUD:

    # ── GET ALL ───────────────────────────────────────────────────────────────
    async def get_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[int, list[HeroSection]]:

        count_result = await db.execute(
            select(func.count())
            .select_from(HeroSection)
            .where(HeroSection.is_deleted == False)
        )
        total = count_result.scalar_one()

        result = await db.execute(
            select(HeroSection)
            .where(HeroSection.is_deleted == False)
            .order_by(HeroSection.display_order.asc())
            .offset(skip)
            .limit(limit)
        )
        heroes = result.scalars().all()

        return total, heroes

    # ── GET BY ID ─────────────────────────────────────────────────────────────
    async def get_by_id(
        self,
        db: AsyncSession,
        hero_id: int,
    ) -> HeroSection | None:

        result = await db.execute(
            select(HeroSection)
            .where(
                HeroSection.id == hero_id,
                HeroSection.is_deleted == False,
            )
        )
        return result.scalar_one_or_none()

    # ── CREATE ────────────────────────────────────────────────────────────────
    # async def create(
    #     self,
    #     db: AsyncSession,
    #     payload: HeroCreate,
    #     background_image: UploadFile | None = None,
    #     hero_image: UploadFile | None = None,
    # ) -> HeroSection:

    #     data = payload.model_dump()

    #     if background_image and background_image.filename:
    #         data["background_image"] = await save_upload(background_image)

    #     if hero_image and hero_image.filename:
    #         data["hero_image"] = await save_upload(hero_image)

    #     hero = HeroSection(**data)
    #     db.add(hero)
    #     await db.commit()
    #     await db.refresh(hero)
    #     return hero


    async def create(
        self,
        db: AsyncSession,
        payload: HeroCreate,
    ) -> HeroSection:

        data = payload.model_dump()

        if data.get("primary_button_url"):
            data["primary_button_url"] = str(data["primary_button_url"])

        if data.get("secondary_button_url"):
            data["secondary_button_url"] = str(data["secondary_button_url"])

        hero = HeroSection(**data)

        db.add(hero)

        await db.commit()

        await db.refresh(hero)

        return hero

    # ── UPDATE ────────────────────────────────────────────────────────────────
    async def update(
        self,
        db: AsyncSession,
        hero: HeroSection,
        payload: HeroUpdate,
        background_image: UploadFile | None = None,
        hero_image: UploadFile | None = None,
    ) -> HeroSection:

        update_data = payload.model_dump(
            exclude_unset=True,
            mode="json",
        )

        for field, value in update_data.items():
            setattr(hero, field, value)

        if background_image and background_image.filename:
            hero.background_image = await save_upload(background_image)

        if hero_image and hero_image.filename:
            hero.hero_image = await save_upload(hero_image)

        hero.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(hero)

        return hero

    # ── DELETE (soft) ─────────────────────────────────────────────────────────
    async def delete(
        self,
        db: AsyncSession,
        hero: HeroSection,
    ) -> None:

        hero.is_deleted = True
        hero.updated_at = datetime.utcnow()
        await db.commit()

    # ── ACTIVATE ──────────────────────────────────────────────────────────────
    async def activate(
        self,
        db: AsyncSession,
        hero: HeroSection,
    ) -> HeroSection:

        # Deactivate all, then activate the target
        await db.execute(
            HeroSection.__table__.update().values(is_active=False)
        )
        hero.is_active = True
        hero.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(hero)
        return hero
    
    # GET ACTIVE HERO
#     # =====================================================

    async def get_active(
        self,
        db: AsyncSession
    ) -> HeroSection | None:

        result = await db.execute(
            select(HeroSection)
            .where(
                HeroSection.is_active == True,
                HeroSection.is_deleted == False
            )
            .order_by(
                HeroSection.display_order.asc()
            )
        )

        return result.scalars().first()


# ── Singleton instance used across routers ────────────────────────────────────
hero_crud = HeroCRUD()












# ---------------------WORKING 100%-----------------------
# from datetime import datetime
# from fastapi import (
#     APIRouter,
#     File,
#     Form,
#     UploadFile,
#     Depends,
#     HTTPException,
#     Query,
#     status,
# )
# from sqlalchemy import select, func
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.models.banner import HeroSection
# from app.schemas.banner import (
#     HeroCreate,
#     HeroUpdate,
# )
# import os
# import uuid
# from pathlib import Path

# class HeroCRUD:

#     # =====================================================
#     # CREATE
#     # =====================================================

#     # async def create(
#     #     self,
#     #     db: AsyncSession,
#     #     payload: HeroCreate
#     # ) -> HeroSection:

#     #     data = payload.model_dump()

#     #     data["primary_button_url"] = str(data["primary_button_url"]) if data.get("primary_button_url") else None
#     #     data["secondary_button_url"] = str(data["secondary_button_url"]) if data.get("secondary_button_url") else None
#     #     data["background_image"] = str(data["background_image"]) if data.get("background_image") else None
#     #     data["hero_image"] = str(data["hero_image"]) if data.get("hero_image") else None

#     #     hero = HeroSection(**data)

#     #     db.add(hero)

#     #     await db.commit()

#     #     await db.refresh(hero)

#     #     return hero

#     async def create(self,db: AsyncSession,data: dict) -> HeroSection:

#         hero = HeroSection(**data)

#         db.add(hero)

#         await db.commit()

#         await db.refresh(hero)

#         return hero

#     # =====================================================
#     # GET BY ID
#     # =====================================================

#     async def get_by_id(
#         self,
#         db: AsyncSession,
#         hero_id: int
#     ) -> HeroSection | None:

#         result = await db.execute(
#             select(HeroSection).where(
#                 HeroSection.id == hero_id,
#                 HeroSection.is_deleted == False
#             )
#         )

#         return result.scalars().first()

#     # =====================================================
#     # GET ACTIVE HERO
#     # =====================================================

#     async def get_active(
#         self,
#         db: AsyncSession
#     ) -> HeroSection | None:

#         result = await db.execute(
#             select(HeroSection)
#             .where(
#                 HeroSection.is_active == True,
#                 HeroSection.is_deleted == False
#             )
#             .order_by(
#                 HeroSection.display_order.asc()
#             )
#         )

#         return result.scalars().first()

#     # =====================================================
#     # GET ALL
#     # =====================================================

#     async def get_all(
#         self,
#         db: AsyncSession,
#         skip: int = 0,
#         limit: int = 20
#     ) -> tuple[int, list[HeroSection]]:

#         total_result = await db.execute(
#             select(func.count())
#             .select_from(HeroSection)
#             .where(
#                 HeroSection.is_deleted == False
#             )
#         )

#         total = total_result.scalar()

#         result = await db.execute(
#             select(HeroSection)
#             .where(
#                 HeroSection.is_deleted == False
#             )
#             .order_by(
#                 HeroSection.display_order.asc()
#             )
#             .offset(skip)
#             .limit(limit)
#         )

#         heroes = result.scalars().all()

#         return total, heroes

#     # =====================================================
#     # UPDATE
#     # =====================================================

#     # async def update(
#     #     self,
#     #     db: AsyncSession,
#     #     hero: HeroSection,
#     #     payload: HeroUpdate
#     # ) -> HeroSection:

#     #     update_data = payload.model_dump(
#     #         exclude_unset=True
#     #     )

#     #     for field, value in update_data.items():
#     #         setattr(hero, field, value)

#     #     hero.updated_at = datetime.utcnow()

#     #     await db.commit()

#     #     await db.refresh(hero)

#     #     return hero




#     UPLOAD_DIR = Path("media/heroes")
#     UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

#     async def save_upload(file: UploadFile) -> str:
#         ext = Path(file.filename).suffix
#         filename = f"{uuid.uuid4().hex}{ext}"
#         path = UPLOAD_DIR / filename
#         content = await file.read()
#         with open(path, "wb") as f:
#             f.write(content)
#         return f"/media/heroes/{filename}"

#     async def update(
#         self,
#         db: AsyncSession,
#         hero: HeroSection,
#         payload: HeroUpdate,
#         background_image: UploadFile | None = None,
#         hero_image: UploadFile | None = None,
#     ) -> HeroSection:

#         update_data = payload.model_dump(exclude_unset=True)

#         for field, value in update_data.items():
#             setattr(hero, field, value)

#         # ✅ Save new images only if a file was actually uploaded
#         if background_image and background_image.filename:
#             hero.background_image = await save_upload(background_image)

#         if hero_image and hero_image.filename:
#             hero.hero_image = await save_upload(hero_image)

#         hero.updated_at = datetime.utcnow()

#         await db.commit()
#         await db.refresh(hero)

#         return hero

#     # =====================================================
#     # SOFT DELETE
#     # =====================================================

#     async def delete(
#         self,
#         db: AsyncSession,
#         hero: HeroSection
#     ) -> bool:

#         hero.is_deleted = True

#         hero.deleted_at = datetime.utcnow()

#         await db.commit()

#         return True

#     # =====================================================
#     # RESTORE
#     # =====================================================

#     async def restore(
#         self,
#         db: AsyncSession,
#         hero_id: int
#     ) -> HeroSection | None:

#         result = await db.execute(
#             select(HeroSection).where(
#                 HeroSection.id == hero_id,
#                 HeroSection.is_deleted == True
#             )
#         )

#         hero = result.scalars().first()

#         if not hero:
#             return None

#         hero.is_deleted = False

#         hero.deleted_at = None

#         await db.commit()

#         await db.refresh(hero)

#         return hero

#     # =====================================================
#     # PERMANENT DELETE
#     # =====================================================

#     async def hard_delete(
#         self,
#         db: AsyncSession,
#         hero_id: int
#     ) -> bool:

#         result = await db.execute(
#             select(HeroSection).where(
#                 HeroSection.id == hero_id
#             )
#         )

#         hero = result.scalars().first()

#         if not hero:
#             return False

#         await db.delete(hero)

#         await db.commit()

#         return True


# hero_crud = HeroCRUD()







# ----------------------------------------------------------------------------------
# from typing import Optional, List

# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.models.banner import Banner


# class BannerCRUD:

#     # ===============================
#     # CREATE BANNER
#     # ===============================
#     async def create_banner(
#         self,
#         db: AsyncSession,
#         **kwargs,
#     ) -> Banner:

#         banner = Banner(**kwargs)
#         db.add(banner)

#         await db.commit()
#         await db.refresh(banner)

#         return banner

#     # ===============================
#     # GET BANNER
#     # ===============================
#     async def get_banner(
#         self,
#         db: AsyncSession,
#         banner_id: int,
#     ) -> Optional[Banner]:

#         stmt = select(Banner).where(Banner.id == banner_id)
#         result = await db.execute(stmt)

#         return result.scalar_one_or_none()

#     # ===============================
#     # LIST ACTIVE BANNERS
#     # ===============================
#     async def get_banners(
#         self,
#         db: AsyncSession,
#     ) -> List[Banner]:

#         stmt = (
#             select(Banner)
#             .where(Banner.is_active.is_(True))
#             .order_by(Banner.display_order.asc())
#         )

#         result = await db.execute(stmt)
#         return result.scalars().all()

#     # ===============================
#     # UPDATE BANNER
#     # ===============================
#     async def update_banner(
#         self,
#         db: AsyncSession,
#         banner: Banner,
#         **kwargs,
#     ) -> Banner:

#         for key, value in kwargs.items():
#             setattr(banner, key, value)

#         await db.commit()
#         await db.refresh(banner)

#         return banner

#     # ===============================
#     # DELETE BANNER
#     # ===============================
#     async def delete_banner(
#         self,
#         db: AsyncSession,
#         banner: Banner,
#     ) -> None:

#         await db.delete(banner)
#         await db.commit()

#     # ===============================
#     # ACTIVATE / DEACTIVATE
#     # ===============================
#     async def toggle_status(
#         self,
#         db: AsyncSession,
#         banner: Banner,
#     ) -> Banner:

#         banner.is_active = not banner.is_active

#         await db.commit()
#         await db.refresh(banner)

#         return banner

#     # ===============================
#     # COUNT BANNERS
#     # ===============================
#     async def count(self, db: AsyncSession) -> int:

#         result = await db.execute(select(Banner))
#         return len(result.scalars().all())


# banner_crud = BannerCRUD()