from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.coupon import Coupon


class CouponCRUD:

    # ===============================
    # CREATE COUPON
    # ===============================
    async def create_coupon(
        self,
        db: AsyncSession,
        **kwargs,
    ) -> Coupon:

        coupon = Coupon(**kwargs)
        db.add(coupon)

        await db.commit()
        await db.refresh(coupon)

        return coupon

    # ===============================
    # GET BY ID
    # ===============================
    async def get_coupon(
        self,
        db: AsyncSession,
        coupon_id: int,
    ) -> Optional[Coupon]:

        stmt = select(Coupon).where(Coupon.id == coupon_id)
        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # ===============================
    # GET BY CODE
    # ===============================
    async def get_by_code(
        self,
        db: AsyncSession,
        code: str,
    ) -> Optional[Coupon]:

        stmt = select(Coupon).where(
            Coupon.code == code,
            Coupon.is_active.is_(True),
        )

        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    # ===============================
    # LIST COUPONS
    # ===============================
    async def get_coupons(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Coupon]:

        stmt = (
            select(Coupon)
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(stmt)
        return result.scalars().all()

    # ===============================
    # UPDATE COUPON
    # ===============================
    async def update_coupon(
        self,
        db: AsyncSession,
        coupon: Coupon,
        **kwargs,
    ) -> Coupon:

        for key, value in kwargs.items():
            setattr(coupon, key, value)

        await db.commit()
        await db.refresh(coupon)

        return coupon

    # ===============================
    # DELETE COUPON
    # ===============================
    async def delete_coupon(
        self,
        db: AsyncSession,
        coupon: Coupon,
    ) -> None:

        await db.delete(coupon)
        await db.commit()

    # ===============================
    # APPLY VALIDATION
    # ===============================
    async def validate_coupon(
        self,
        db: AsyncSession,
        code: str,
        order_amount: float,
    ) -> tuple[bool, Optional[Coupon], str]:

        coupon = await self.get_by_code(db, code)

        if not coupon:
            return False, None, "Invalid coupon"

        if not coupon.is_active:
            return False, None, "Coupon inactive"

        if coupon.expiry_date < coupon.created_at:
            return False, None, "Coupon expired"

        if coupon.current_uses >= coupon.max_uses:
            return False, None, "Coupon usage limit reached"

        if order_amount < coupon.min_order_amount:
            return False, None, "Minimum order not met"

        return True, coupon, "Valid coupon"

    # ===============================
    # INCREMENT USAGE
    # ===============================
    async def increment_usage(
        self,
        db: AsyncSession,
        coupon: Coupon,
    ):

        coupon.current_uses += 1
        await db.commit()

    # ===============================
    # COUPON STATS
    # ===============================
    async def stats(
        self,
        db: AsyncSession,
    ):

        total = await db.scalar(select(func.count(Coupon.id)))
        active = await db.scalar(
            select(func.count(Coupon.id)).where(Coupon.is_active.is_(True))
        )

        return {
            "total_coupons": total or 0,
            "active_coupons": active or 0,
        }


coupon_crud = CouponCRUD()