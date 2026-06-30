from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.curd.category import category_crud
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)


class CategoryService:

    async def create_category(
        self,
        db: AsyncSession,
        payload: CategoryCreate,
    ):
        existing = await category_crud.get_by_name(
            db,
            payload.name,
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Category already exists",
            )

        return await category_crud.create(
            db,
            name=payload.name,
            description=payload.description,
            image_url=payload.image_url,
        )

    async def get_categories(
        self,
        db: AsyncSession,
    ):
        return await category_crud.get_all(db)

    async def get_category(
        self,
        db: AsyncSession,
        category_id: int,
    ):
        category = await category_crud.get_by_id(
            db,
            category_id,
        )

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )

        return category


category_service = CategoryService()