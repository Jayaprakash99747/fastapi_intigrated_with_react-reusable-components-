# app/api/routers/categories.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.product import Category
from sqlalchemy import select

router = APIRouter(prefix="/categories", tags=["Categories"])


# =====================================================
# GET ALL CATEGORIES
# =====================================================

@router.get("/")
async def get_categories(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Category))
    categories = result.scalars().all()

    return categories


# =====================================================
# CREATE CATEGORY
# =====================================================

@router.post("/")
async def create_category(
    name: str,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Category).where(Category.name == name)
    )

    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    category = Category(name=name)

    db.add(category)
    await db.commit()
    await db.refresh(category)

    return {
        "message": "Category created",
        "id": category.id,
        "name": category.name
    }