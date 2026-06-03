from typing import List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc, asc

from app.models.product import Product
# from app.models. import Category
from sqlalchemy.ext.asyncio import AsyncSession
from app.curd.product import product_crud



class ProductService:

    # =====================================================
    # GET PRODUCT BY ID
    # =====================================================

    async def get_product(
        self,
        db: AsyncSession,
        product_id: int,
    ) -> Optional[Product]:

        stmt = select(Product).where(
            Product.id == product_id,
            Product.is_deleted.is_(False),
        )

        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    # =====================================================
    # LIST PRODUCTS (WITH FILTERS)
    # =====================================================

    async def list_products(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort_by: str = "created_at",
        order: str = "desc",
    ) -> List[Product]:

        stmt = select(Product).where(
            Product.is_deleted.is_(False),
            Product.is_available.is_(True),
        )

        # -----------------------------
        # CATEGORY FILTER
        # -----------------------------
        if category_id:
            stmt = stmt.where(Product.category_id == category_id)

        # -----------------------------
        # PRICE FILTER
        # -----------------------------
        if min_price is not None:
            stmt = stmt.where(Product.price >= min_price)

        if max_price is not None:
            stmt = stmt.where(Product.price <= max_price)

        # -----------------------------
        # SORTING
        # -----------------------------
        sort_column = getattr(Product, sort_by, Product.created_at)

        if order == "asc":
            stmt = stmt.order_by(asc(sort_column))
        else:
            stmt = stmt.order_by(desc(sort_column))

        stmt = stmt.offset(skip).limit(limit)

        result = await db.execute(stmt)
        return result.scalars().all()

    # =====================================================
    # SEARCH PRODUCTS (FAST ILIKE)
    # =====================================================

    async def search_products(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 20,
    ) -> List[Product]:

        stmt = select(Product).where(
            Product.is_deleted.is_(False),
            or_(
                Product.name.ilike(f"%{query}%"),
                Product.description.ilike(f"%{query}%"),
                Product.brand.ilike(f"%{query}%"),
            ),
        ).limit(limit)

        result = await db.execute(stmt)
        return result.scalars().all()

    # =====================================================
    # FEATURED PRODUCTS
    # =====================================================

    async def get_featured_products(
        self,
        db: AsyncSession,
        limit: int = 10,
    ) -> List[Product]:

        stmt = select(Product).where(
            Product.is_deleted.is_(False),
            Product.is_featured.is_(True),
        ).limit(limit)

        result = await db.execute(stmt)
        return result.scalars().all()

    # =====================================================
    # PRODUCTS BY CATEGORY
    # =====================================================

    async def get_by_category(
        self,
        db: AsyncSession,
        category_id: int,
        limit: int = 20,
    ) -> List[Product]:

        stmt = select(Product).where(
            Product.category_id == category_id,
            Product.is_deleted.is_(False),
        ).limit(limit)

        result = await db.execute(stmt)
        return result.scalars().all()

    # =====================================================
    # CREATE PRODUCT (ADMIN)
    # =====================================================

    async def create_product(
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
    # UPDATE PRODUCT
    # =====================================================

    async def update_product(
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

    async def delete_product(
        self,
        db: AsyncSession,
        product: Product,
    ) -> None:

        product.is_deleted = True

        await db.commit()

    # =====================================================
    # UPDATE RATING
    # =====================================================

    async def update_rating(
        self,
        db: AsyncSession,
        product: Product,
        new_rating: float,
    ) -> Product:

        product.rating = new_rating

        await db.commit()
        await db.refresh(product)

        return product

    # =====================================================
    # PRODUCT STATS
    # =====================================================

    async def product_stats(self, db: AsyncSession):

        total_products = len(await self.list_products(db, limit=100000))
        featured = len(await self.get_featured_products(db, limit=100000))

        return {
            "total_products": total_products,
            "featured_products": featured,
        }

# --------------------------------------------------

    # =====================================================
    # CREATE PRODUCT
    # =====================================================
    async def create_product(self, db: AsyncSession, payload):

        product = await product_crud.create(
            db,
            category_id=payload.category_id,
            name=payload.name,
            description=payload.description,
            brand=payload.brand,
            sku=payload.sku,
            price=payload.price,
            discount_percent=payload.discount_percent,
            gst_percent=payload.gst_percent,
            stock_quantity=payload.stock_quantity,
            is_available=payload.is_available,
            is_featured=payload.is_featured,
        )

        # images
        for img in payload.images:
            await product_crud.create_image(
                db,
                product_id=product.id,
                image_url=img.image_url,
                is_primary=img.is_primary,
            )

        return product


    # =====================================================
    # GET PRODUCT
    # =====================================================
    async def get_product(self, db, product_id: int):
        return await product_crud.get_by_id(db, product_id)


    # =====================================================
    # LIST PRODUCTS
    # =====================================================
    async def get_all_products(self, db, skip: int, limit: int):
        return await product_crud.get_all(db, skip, limit)


    # =====================================================
    # SEARCH
    # =====================================================
    async def search_products(self, db, keyword: str):
        return await product_crud.search(db, keyword)


    # =====================================================
    # FILTER
    # =====================================================
    async def filter_products(self, db, payload):
        return await product_crud.filter_products(
            db,
            category_id=payload.category_id,
            brand=payload.brand,
            min_price=payload.min_price,
            max_price=payload.max_price,
            min_rating=payload.min_rating,
            is_featured=payload.is_featured,
            is_available=payload.is_available,
        )


    # =====================================================
    # FEATURED
    # =====================================================
    async def featured_products(self, db):
        return await product_crud.featured_products(db)


    # =====================================================
    # UPDATE
    # =====================================================
    async def update_product(self, db, product_id: int, payload):

        product = await product_crud.get_by_id(db, product_id)

        return await product_crud.update(
            db,
            product,
            **payload.model_dump(exclude_unset=True),
        )


    # =====================================================
    # DELETE (SOFT DELETE)
    # =====================================================
    async def delete_product(self, db, product_id: int):

        product = await product_crud.get_by_id(db, product_id)
        return await product_crud.delete(db, product)


    # =====================================================
    # RESTORE
    # =====================================================
    async def restore_product(self, db, product_id: int):

        product = await product_crud.get_by_id(db, product_id)
        return await product_crud.restore(db, product)


    # =====================================================
    # STATS
    # =====================================================
    async def get_stats(self, db):
        return await product_crud.stats(db)




product_service = ProductService()