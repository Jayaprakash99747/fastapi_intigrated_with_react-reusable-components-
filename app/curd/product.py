from typing import Optional

from sqlalchemy import (
    select,
    func,
    and_,
    or_,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    selectinload,
)

from app.models.product import (
    Product,
    ProductImage,
    Category,
)


class ProductCRUD:

    # =====================================================
    # CREATE PRODUCT
    # =====================================================

    async def create(
        self,
        db: AsyncSession,
        **kwargs,
    ) -> Product:

        product = Product(**kwargs)

        db.add(product)

        await db.commit()

        await db.refresh(product)

        return product

    # =====================================================
    # CREATE PRODUCT IMAGE
    # =====================================================

    async def create_image(
        self,
        db: AsyncSession,
        product_id: int,
        image_url: str,
        is_primary: bool = False,
    ) -> ProductImage:

        image = ProductImage(
            product_id=product_id,
            image_url=image_url,
            is_primary=is_primary,
        )

        db.add(image)

        await db.commit()

        await db.refresh(image)

        return image

    # =====================================================
    # GET PRODUCT
    # =====================================================

    async def get_by_id(
        self,
        db: AsyncSession,
        product_id: int,
    ) -> Optional[Product]:

        stmt = (
            select(Product)
            .options(
                selectinload(Product.images),
                selectinload(Product.category),
                selectinload(Product.inventory),
                selectinload(Product.reviews),
            )
            .where(
                Product.id == product_id,
                Product.is_deleted.is_(False),
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # GET PRODUCT BY NAME
    # =====================================================

    async def get_by_name(
        self,
        db: AsyncSession,
        name: str,
    ) -> Optional[Product]:

        stmt = (
            select(Product)
            .where(
                func.lower(Product.name)
                == name.lower(),
                Product.is_deleted.is_(False),
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # LIST PRODUCTS
    # =====================================================

    async def get_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
    ):

        stmt = (
            select(Product)
            .options(
                selectinload(Product.images),
                selectinload(Product.category),
            )
            .where(
                Product.is_deleted.is_(False)
            )
            .order_by(
                Product.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # SEARCH PRODUCTS
    # =====================================================

    async def search(
        self,
        db: AsyncSession,
        keyword: str,
        skip: int = 0,
        limit: int = 20,
    ):

        stmt = (
            select(Product)
            .options(
                selectinload(Product.images)
            )
            .where(
                and_(
                    Product.is_deleted.is_(False),
                    or_(
                        Product.name.ilike(
                            f"%{keyword}%"
                        ),
                        Product.description.ilike(
                            f"%{keyword}%"
                        ),
                        Product.brand.ilike(
                            f"%{keyword}%"
                        ),
                    ),
                )
            )
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # FEATURED PRODUCTS
    # =====================================================

    async def featured_products(
        self,
        db: AsyncSession,
        limit: int = 20,
    ):

        stmt = (
            select(Product)
            .options(
                selectinload(Product.images)
            )
            .where(
                Product.is_featured.is_(True),
                Product.is_deleted.is_(False),
                Product.is_available.is_(True),
            )
            .limit(limit)
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # PRODUCTS BY CATEGORY
    # =====================================================

    async def get_by_category(
        self,
        db: AsyncSession,
        category_id: int,
        skip: int = 0,
        limit: int = 20,
    ):

        stmt = (
            select(Product)
            .options(
                selectinload(Product.images)
            )
            .where(
                Product.category_id == category_id,
                Product.is_deleted.is_(False),
            )
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # FILTER PRODUCTS
    # =====================================================

    async def filter_products(
        self,
        db: AsyncSession,
        *,
        category_id: int | None = None,
        brand: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_rating: float | None = None,
        is_featured: bool | None = None,
        is_available: bool | None = None,
        skip: int = 0,
        limit: int = 20,
    ):

        filters = [
            Product.is_deleted.is_(False)
        ]

        if category_id:
            filters.append(
                Product.category_id == category_id
            )

        if brand:
            filters.append(
                Product.brand.ilike(
                    f"%{brand}%"
                )
            )

        if min_price is not None:
            filters.append(
                Product.price >= min_price
            )

        if max_price is not None:
            filters.append(
                Product.price <= max_price
            )

        if min_rating is not None:
            filters.append(
                Product.rating >= min_rating
            )

        if is_featured is not None:
            filters.append(
                Product.is_featured == is_featured
            )

        if is_available is not None:
            filters.append(
                Product.is_available == is_available
            )

        stmt = (
            select(Product)
            .options(
                selectinload(Product.images)
            )
            .where(*filters)
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # UPDATE PRODUCT
    # =====================================================

    async def update(
        self,
        db: AsyncSession,
        product: Product,
        **kwargs,
    ) -> Product:

        for key, value in kwargs.items():
            setattr(product, key, value)

        await db.commit()

        await db.refresh(product)

        return product

    # =====================================================
    # SOFT DELETE PRODUCT
    # =====================================================

    async def delete(
        self,
        db: AsyncSession,
        product: Product,
    ):

        product.is_deleted = True

        await db.commit()

    # =====================================================
    # RESTORE PRODUCT
    # =====================================================

    async def restore(
        self,
        db: AsyncSession,
        product: Product,
    ):

        product.is_deleted = False

        await db.commit()

        await db.refresh(product)

        return product

    # =====================================================
    # DELETE PRODUCT IMAGE
    # =====================================================

    async def delete_image(
        self,
        db: AsyncSession,
        image_id: int,
    ):

        stmt = (
            select(ProductImage)
            .where(
                ProductImage.id == image_id
            )
        )

        result = await db.execute(stmt)

        image = result.scalar_one_or_none()

        if image:
            await db.delete(image)
            await db.commit()

    # =====================================================
    # PRODUCT COUNT
    # =====================================================

    async def count(
        self,
        db: AsyncSession,
    ) -> int:

        stmt = (
            select(
                func.count(Product.id)
            )
            .where(
                Product.is_deleted.is_(False)
            )
        )

        result = await db.execute(stmt)

        return result.scalar() or 0

    # =====================================================
    # PRODUCT STATS
    # =====================================================

    async def stats(
        self,
        db: AsyncSession,
    ):

        total_products = await db.scalar(
            select(func.count(Product.id))
            .where(Product.is_deleted.is_(False))
        )

        featured_products = await db.scalar(
            select(func.count(Product.id))
            .where(
                Product.is_featured.is_(True),
                Product.is_deleted.is_(False),
            )
        )

        available_products = await db.scalar(
            select(func.count(Product.id))
            .where(
                Product.is_available.is_(True),
                Product.is_deleted.is_(False),
            )
        )

        return {
            "total_products": total_products or 0,
            "featured_products": featured_products or 0,
            "available_products": available_products or 0,
        }

    # =====================================================
    # CATEGORY EXISTS
    # =====================================================

    async def category_exists(
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


product_crud = ProductCRUD()