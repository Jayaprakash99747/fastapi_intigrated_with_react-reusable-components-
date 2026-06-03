from typing import Optional

from sqlalchemy import (
    select,
    update,
    func,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.product import (
    Category,
    Product,
)


class CategoryCRUD:

    # =====================================================
    # CREATE CATEGORY
    # =====================================================

    async def create(
        self,
        db: AsyncSession,
        **kwargs,
    ) -> Category:

        category = Category(**kwargs)

        db.add(category)

        await db.commit()

        await db.refresh(category)

        return category

    # =====================================================
    # GET CATEGORY BY ID
    # =====================================================

    async def get_by_id(
        self,
        db: AsyncSession,
        category_id: int,
    ) -> Optional[Category]:

        stmt = (
            select(Category)
            .options(
                selectinload(Category.products)
            )
            .where(
                Category.id == category_id,
                Category.is_deleted.is_(False),
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # GET CATEGORY BY NAME
    # =====================================================

    async def get_by_name(
        self,
        db: AsyncSession,
        name: str,
    ) -> Optional[Category]:

        stmt = (
            select(Category)
            .where(
                func.lower(Category.name)
                == name.lower(),
                Category.is_deleted.is_(False),
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # GET ALL CATEGORIES
    # =====================================================

    async def get_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
    ):

        stmt = (
            select(Category)
            .where(
                Category.is_deleted.is_(False)
            )
            .order_by(
                Category.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # SEARCH CATEGORIES
    # =====================================================

    async def search(
        self,
        db: AsyncSession,
        keyword: str,
        skip: int = 0,
        limit: int = 20,
    ):

        stmt = (
            select(Category)
            .where(
                Category.name.ilike(
                    f"%{keyword}%"
                ),
                Category.is_deleted.is_(False),
            )
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # UPDATE CATEGORY
    # =====================================================

    async def update(
        self,
        db: AsyncSession,
        category: Category,
        **kwargs,
    ) -> Category:

        for key, value in kwargs.items():
            setattr(category, key, value)

        await db.commit()

        await db.refresh(category)

        return category

    # =====================================================
    # SOFT DELETE CATEGORY
    # =====================================================

    async def delete(
        self,
        db: AsyncSession,
        category: Category,
    ) -> None:

        category.is_deleted = True

        await db.commit()

    # =====================================================
    # RESTORE CATEGORY
    # =====================================================

    async def restore(
        self,
        db: AsyncSession,
        category: Category,
    ) -> Category:

        category.is_deleted = False

        await db.commit()

        await db.refresh(category)

        return category

    # =====================================================
    # CATEGORY EXISTS
    # =====================================================

    async def exists(
        self,
        db: AsyncSession,
        category_id: int,
    ) -> bool:

        stmt = (
            select(Category.id)
            .where(
                Category.id == category_id,
                Category.is_deleted.is_(False),
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none() is not None

    # =====================================================
    # TOTAL COUNT
    # =====================================================

    async def count(
        self,
        db: AsyncSession,
    ) -> int:

        stmt = (
            select(
                func.count(Category.id)
            )
            .where(
                Category.is_deleted.is_(False)
            )
        )

        result = await db.execute(stmt)

        return result.scalar() or 0

    # =====================================================
    # CATEGORY WITH PRODUCT COUNT
    # =====================================================

    async def get_with_product_count(
        self,
        db: AsyncSession,
    ):

        stmt = (
            select(
                Category.id,
                Category.name,
                func.count(Product.id)
                .label("product_count")
            )
            .outerjoin(
                Product,
                Product.category_id
                == Category.id
            )
            .where(
                Category.is_deleted.is_(False)
            )
            .group_by(
                Category.id
            )
        )

        result = await db.execute(stmt)

        return result.all()


category_crud = CategoryCRUD()