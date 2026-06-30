# # app/api/routers/categories.py

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.db.session import get_db
# from app.models.product import Category
# from sqlalchemy import select

# router = APIRouter(prefix="/categories", tags=["Categories"])


# # =====================================================
# # GET ALL CATEGORIES
# # =====================================================

# @router.get("/")
# async def get_categories(db: AsyncSession = Depends(get_db)):

#     result = await db.execute(select(Category))
#     categories = result.scalars().all()

#     return categories


# # =====================================================
# # CREATE CATEGORY
# # =====================================================

# @router.post("/")
# async def create_category(
#     name: str,
#     db: AsyncSession = Depends(get_db),
# ):

#     result = await db.execute(
#         select(Category).where(Category.name == name)
#     )

#     existing = result.scalar_one_or_none()

#     if existing:
#         raise HTTPException(
#             status_code=400,
#             detail="Category already exists"
#         )

#     category = Category(name=name)

#     db.add(category)
#     await db.commit()
#     await db.refresh(category)

#     return {
#         "message": "Category created",
#         "id": category.id,
#         "name": category.name
#     }



from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.services.category_service import (
    category_service,
)

from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)

from app.permissions.roles import (
    require_admin,
    require_user,
)

from app.models.user import User

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

@router.get(
    "/",
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_categories(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: AsyncSession = Depends(get_db),
):
    return await category_service.get_categories(
        db=db,
        skip=skip,
        limit=limit,
    )



@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await category_service.get_category(
        db=db,
        category_id=category_id,
    )

@router.get(
    "/search/{keyword}",
    response_model=list[CategoryResponse],
)
async def search_categories(
    keyword: str,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    return await category_service.search_categories(
        db=db,
        keyword=keyword,
        skip=skip,
        limit=limit,
    )

@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    payload: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_admin
    ),
):
    return await category_service.create_category(
        db=db,
        payload=payload,
    )

@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
async def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_admin
    ),
):
    return await category_service.update_category(
        db=db,
        category_id=category_id,
        payload=payload,
    )


@router.delete(
    "/{category_id}",
)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_admin
    ),
):
    return await category_service.delete_category(
        db=db,
        category_id=category_id,
    )

@router.patch(
    "/{category_id}/restore",
)
async def restore_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_admin
    ),
):
    return await category_service.restore_category(
        db=db,
        category_id=category_id,
    )


@router.get(
    "/admin/stats",
)
async def category_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_admin
    ),
):
    return await category_service.category_stats(
        db
    )