from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.product_service import product_service
from app.services.auth_service import AuthService

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
    ProductDetailResponse,
    ProductSearchRequest,
    ProductFilterRequest,
    ProductDeleteResponse,
    ProductStatsResponse,
)

router = APIRouter(prefix="/products", tags=["Products"])


# =====================================================
# 🟢 1. GET ALL PRODUCTS (PUBLIC)
# =====================================================
@router.get("/", response_model=ProductListResponse)
async def get_products(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
):
    items = await product_service.get_all_products(db, skip, limit)
    return {"items": items}


# =====================================================
# 🟢 2. GET PRODUCT BY ID (PUBLIC)
# =====================================================
@router.get("/{product_id}", response_model=ProductDetailResponse)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await product_service.get_product(db, product_id)


# =====================================================
# 🟢 3. SEARCH PRODUCTS
# =====================================================
@router.get("/search", response_model=ProductListResponse)
async def search_products(
    keyword: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    items = await product_service.search_products(db, keyword)
    return {"items": items}


# =====================================================
# 🟢 4. FILTER PRODUCTS
# =====================================================
@router.post("/filter", response_model=ProductListResponse)
async def filter_products(
    payload: ProductFilterRequest,
    db: AsyncSession = Depends(get_db),
):
    items = await product_service.filter_products(db, payload)
    return {"items": items}


# =====================================================
# 🟢 5. FEATURED PRODUCTS
# =====================================================
@router.get("/featured", response_model=ProductListResponse)
async def featured_products(db: AsyncSession = Depends(get_db)):
    items = await product_service.featured_products(db)
    return {"items": items}