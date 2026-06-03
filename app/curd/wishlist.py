from typing import Optional

from sqlalchemy import (
    select,
    func,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    selectinload,
)

from app.models.product import (
    Product,
    WishlistItem,
)


class WishlistCRUD:

    # =====================================================
    # ADD TO WISHLIST
    # =====================================================

    async def add_to_wishlist(
        self,
        db: AsyncSession,
        user_id: int,
        product_id: int,
    ) -> WishlistItem:

        stmt = (
            select(WishlistItem)
            .where(
                WishlistItem.user_id == user_id,
                WishlistItem.product_id == product_id,
            )
        )

        result = await db.execute(stmt)

        existing = result.scalar_one_or_none()

        if existing:
            return existing

        wishlist_item = WishlistItem(
            user_id=user_id,
            product_id=product_id,
        )

        db.add(wishlist_item)

        await db.commit()

        await db.refresh(wishlist_item)

        return wishlist_item

    # =====================================================
    # GET USER WISHLIST
    # =====================================================

    async def get_wishlist(
        self,
        db: AsyncSession,
        user_id: int,
    ):

        stmt = (
            select(WishlistItem)
            .options(
                selectinload(WishlistItem.product)
                .selectinload(Product.images)
            )
            .where(
                WishlistItem.user_id == user_id
            )
            .order_by(
                WishlistItem.created_at.desc()
            )
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # GET WISHLIST ITEM
    # =====================================================

    async def get_item(
        self,
        db: AsyncSession,
        wishlist_id: int,
        user_id: int,
    ) -> Optional[WishlistItem]:

        stmt = (
            select(WishlistItem)
            .options(
                selectinload(WishlistItem.product)
            )
            .where(
                WishlistItem.id == wishlist_id,
                WishlistItem.user_id == user_id,
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # REMOVE FROM WISHLIST
    # =====================================================

    async def remove_from_wishlist(
        self,
        db: AsyncSession,
        wishlist_item: WishlistItem,
    ) -> None:

        await db.delete(wishlist_item)

        await db.commit()

    # =====================================================
    # CLEAR WISHLIST
    # =====================================================

    async def clear_wishlist(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> None:

        stmt = (
            select(WishlistItem)
            .where(
                WishlistItem.user_id == user_id
            )
        )

        result = await db.execute(stmt)

        items = result.scalars().all()

        for item in items:
            await db.delete(item)

        await db.commit()

    # =====================================================
    # PRODUCT EXISTS
    # =====================================================

    async def product_exists(
        self,
        db: AsyncSession,
        product_id: int,
    ) -> bool:

        stmt = (
            select(Product.id)
            .where(
                Product.id == product_id,
                Product.is_deleted.is_(False),
                Product.is_available.is_(True),
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none() is not None

    # =====================================================
    # GET PRODUCT
    # =====================================================

    async def get_product(
        self,
        db: AsyncSession,
        product_id: int,
    ) -> Optional[Product]:

        stmt = (
            select(Product)
            .options(
                selectinload(Product.images)
            )
            .where(
                Product.id == product_id,
                Product.is_deleted.is_(False),
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # CHECK PRODUCT IN WISHLIST
    # =====================================================

    async def exists(
        self,
        db: AsyncSession,
        user_id: int,
        product_id: int,
    ) -> bool:

        stmt = (
            select(WishlistItem.id)
            .where(
                WishlistItem.user_id == user_id,
                WishlistItem.product_id == product_id,
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none() is not None

    # =====================================================
    # WISHLIST COUNT
    # =====================================================

    async def wishlist_count(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> int:

        stmt = (
            select(
                func.count(WishlistItem.id)
            )
            .where(
                WishlistItem.user_id == user_id
            )
        )

        result = await db.execute(stmt)

        return result.scalar() or 0

    # =====================================================
    # MOVE WISHLIST TO CART CHECK
    # =====================================================

    async def get_wishlist_product_ids(
        self,
        db: AsyncSession,
        user_id: int,
    ):

        stmt = (
            select(
                WishlistItem.product_id
            )
            .where(
                WishlistItem.user_id == user_id
            )
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # WISHLIST SUMMARY
    # =====================================================

    async def wishlist_summary(
        self,
        db: AsyncSession,
        user_id: int,
    ):

        items = await self.get_wishlist(
            db=db,
            user_id=user_id,
        )

        total_products = len(items)

        total_value = 0

        for item in items:

            if item.product:
                total_value += item.product.price

        return {
            "total_products": total_products,
            "total_value": round(
                total_value,
                2,
            ),
        }


wishlist_crud = WishlistCRUD()