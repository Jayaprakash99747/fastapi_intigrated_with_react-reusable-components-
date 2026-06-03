from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.product import Product
from app.models.user import User
from app.models.review import Review


class ReviewCRUD:

    # =====================================================
    # CREATE REVIEW
    # =====================================================

    async def create_review(
        self,
        db: AsyncSession,
        user_id: int,
        product_id: int,
        rating: int,
        comment: str | None = None,
        is_verified_purchase: bool = False,
    ) -> Review:

        review = Review(
            user_id=user_id,
            product_id=product_id,
            rating=rating,
            comment=comment,
            is_verified_purchase=is_verified_purchase,
        )

        db.add(review)
        await db.commit()
        await db.refresh(review)

        # update product rating after review creation
        await self._recalculate_product_rating(db, product_id)

        return review

    # =====================================================
    # GET REVIEW BY ID
    # =====================================================

    async def get_review(
        self,
        db: AsyncSession,
        review_id: int,
    ) -> Optional[Review]:

        stmt = (
            select(Review)
            .options(
                selectinload(Review.user),
                selectinload(Review.product),
            )
            .where(Review.id == review_id)
        )

        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    # =====================================================
    # GET REVIEWS FOR PRODUCT
    # =====================================================

    async def get_product_reviews(
        self,
        db: AsyncSession,
        product_id: int,
        skip: int = 0,
        limit: int = 20,
    ):

        stmt = (
            select(Review)
            .options(selectinload(Review.user))
            .where(Review.product_id == product_id)
            .order_by(Review.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(stmt)
        return result.scalars().all()

    # =====================================================
    # UPDATE REVIEW
    # =====================================================

    async def update_review(
        self,
        db: AsyncSession,
        review: Review,
        rating: Optional[int] = None,
        comment: Optional[str] = None,
    ) -> Review:

        if rating is not None:
            review.rating = rating

        if comment is not None:
            review.comment = comment

        await db.commit()
        await db.refresh(review)

        await self._recalculate_product_rating(db, review.product_id)

        return review

    # =====================================================
    # DELETE REVIEW
    # =====================================================

    async def delete_review(
        self,
        db: AsyncSession,
        review: Review,
    ) -> None:

        product_id = review.product_id

        await db.delete(review)
        await db.commit()

        await self._recalculate_product_rating(db, product_id)

    # =====================================================
    # CHECK IF USER ALREADY REVIEWED PRODUCT
    # =====================================================

    async def review_exists(
        self,
        db: AsyncSession,
        user_id: int,
        product_id: int,
    ) -> bool:

        stmt = select(Review.id).where(
            Review.user_id == user_id,
            Review.product_id == product_id,
        )

        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None

    # =====================================================
    # PRODUCT RATING STATS
    # =====================================================

    async def rating_stats(
        self,
        db: AsyncSession,
        product_id: int,
    ):

        stmt = select(
            func.count(Review.id),
            func.avg(Review.rating),
        ).where(Review.product_id == product_id)

        result = await db.execute(stmt)
        total, avg_rating = result.first()

        return {
            "total_reviews": total or 0,
            "average_rating": float(avg_rating or 0),
        }

    # =====================================================
    # CALCULATE PRODUCT RATING (INTERNAL)
    # =====================================================

    async def _recalculate_product_rating(
        self,
        db: AsyncSession,
        product_id: int,
    ) -> None:

        stmt = select(func.avg(Review.rating)).where(
            Review.product_id == product_id
        )

        result = await db.execute(stmt)
        avg_rating = result.scalar()

        stmt_count = select(func.count(Review.id)).where(
            Review.product_id == product_id
        )

        result_count = await db.execute(stmt_count)
        total_reviews = result_count.scalar() or 0

        stmt_product = select(Product).where(Product.id == product_id)
        result_product = await db.execute(stmt_product)
        product = result_product.scalar_one_or_none()

        if product:
            product.rating = float(avg_rating or 0)
            await db.commit()

    # =====================================================
    # GET USER REVIEW
    # =====================================================

    async def get_user_review(
        self,
        db: AsyncSession,
        user_id: int,
        product_id: int,
    ) -> Optional[Review]:

        stmt = select(Review).where(
            Review.user_id == user_id,
            Review.product_id == product_id,
        )

        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    # =====================================================
    # REVIEW COUNT FOR PRODUCT
    # =====================================================

    async def review_count(
        self,
        db: AsyncSession,
        product_id: int,
    ) -> int:

        stmt = select(func.count(Review.id)).where(
            Review.product_id == product_id
        )

        result = await db.execute(stmt)
        return result.scalar() or 0

    # =====================================================
    # RECENT REVIEWS
    # =====================================================

    async def recent_reviews(
        self,
        db: AsyncSession,
        limit: int = 10,
    ):

        stmt = (
            select(Review)
            .options(
                selectinload(Review.user),
                selectinload(Review.product),
            )
            .order_by(Review.created_at.desc())
            .limit(limit)
        )

        result = await db.execute(stmt)
        return result.scalars().all()


review_crud = ReviewCRUD()