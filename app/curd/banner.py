from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.banner import Banner


class BannerCRUD:

    # ===============================
    # CREATE BANNER
    # ===============================
    async def create_banner(
        self,
        db: AsyncSession,
        **kwargs,
    ) -> Banner:

        banner = Banner(**kwargs)
        db.add(banner)

        await db.commit()
        await db.refresh(banner)

        return banner

    # ===============================
    # GET BANNER
    # ===============================
    async def get_banner(
        self,
        db: AsyncSession,
        banner_id: int,
    ) -> Optional[Banner]:

        stmt = select(Banner).where(Banner.id == banner_id)
        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # ===============================
    # LIST ACTIVE BANNERS
    # ===============================
    async def get_banners(
        self,
        db: AsyncSession,
    ) -> List[Banner]:

        stmt = (
            select(Banner)
            .where(Banner.is_active.is_(True))
            .order_by(Banner.display_order.asc())
        )

        result = await db.execute(stmt)
        return result.scalars().all()

    # ===============================
    # UPDATE BANNER
    # ===============================
    async def update_banner(
        self,
        db: AsyncSession,
        banner: Banner,
        **kwargs,
    ) -> Banner:

        for key, value in kwargs.items():
            setattr(banner, key, value)

        await db.commit()
        await db.refresh(banner)

        return banner

    # ===============================
    # DELETE BANNER
    # ===============================
    async def delete_banner(
        self,
        db: AsyncSession,
        banner: Banner,
    ) -> None:

        await db.delete(banner)
        await db.commit()

    # ===============================
    # ACTIVATE / DEACTIVATE
    # ===============================
    async def toggle_status(
        self,
        db: AsyncSession,
        banner: Banner,
    ) -> Banner:

        banner.is_active = not banner.is_active

        await db.commit()
        await db.refresh(banner)

        return banner

    # ===============================
    # COUNT BANNERS
    # ===============================
    async def count(self, db: AsyncSession) -> int:

        result = await db.execute(select(Banner))
        return len(result.scalars().all())


banner_crud = BannerCRUD()