from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.order_service import order_service
from app.services.auth_service import AuthService
from app.schemas.order import (
    OrderListResponse,
    OrderDetailResponse,
    OrderStatusUpdate,
    OrderSummaryResponse,
)
from app.api.dependencies import get_admin_user

router = APIRouter(prefix="/orders/admin", tags=["Admin Orders"])


# =====================================================
# 1. GET ALL ORDERS (ADMIN READ)
# =====================================================
@router.get("/", response_model=OrderListResponse)
async def get_all_orders(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
    skip: int = 0,
    limit: int = 50,
):
    items = await order_service.get_all_orders(
        db=db,
        skip=skip,
        limit=limit,
    )
    return {"items": items}


# =====================================================
# 2. GET ORDER BY ID (ADMIN READ)
# =====================================================
@router.get("/{order_id}", response_model=OrderDetailResponse)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return await order_service.get_order(db, order_id)


# =====================================================
# 3. UPDATE ORDER STATUS (ADMIN UPDATE)
# =====================================================
@router.patch("/{order_id}/status")
async def update_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return await order_service.update_status(
        db=db,
        order_id=order_id,
        status=payload.status,
    )


# =====================================================
# 4. UPDATE TRACKING NUMBER
# =====================================================
@router.patch("/{order_id}/tracking")
async def update_tracking(
    order_id: int,
    tracking_number: str = Query(...),
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return await order_service.update_tracking(
        db=db,
        order_id=order_id,
        tracking_number=tracking_number,
    )


# =====================================================
# 5. DELETE ORDER (ADMIN DELETE)
# =====================================================
@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return await order_service.delete_order(
        db=db,
        order_id=order_id,
    )


# =====================================================
# 6. FILTER ORDERS BY STATUS (ADMIN READ FILTER)
# =====================================================
@router.get("/status/{status}", response_model=OrderListResponse)
async def orders_by_status(
    status: str,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
    skip: int = 0,
    limit: int = 50,
):
    items = await order_service.get_orders_by_status(
        db=db,
        status=status,
        skip=skip,
        limit=limit,
    )
    return {"items": items}


# =====================================================
# 7. ORDER DASHBOARD SUMMARY (ADMIN ANALYTICS)
# =====================================================
@router.get("/summary", response_model=OrderSummaryResponse)
async def order_summary(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return await order_service.order_summary(db)


# =====================================================
# 8. CANCEL ORDER (ADMIN FORCE CANCEL)
# =====================================================
@router.patch("/{order_id}/cancel")
async def admin_cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return await order_service.cancel_order(
        db=db,
        order_id=order_id,
        admin_override=True,
    )




# router/product_admin.py


from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.product_service import product_service
from app.services.auth_service import AuthService

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductDeleteResponse,
    ProductStatsResponse,
)

router = APIRouter(prefix="/admin/products", tags=["Admin Products"])


# =====================================================
# 🛠 1. CREATE PRODUCT (ADMIN)
# =====================================================
@router.post("/", response_model=ProductResponse)
async def create_product(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return await product_service.create_product(db, payload)


# =====================================================
# 🛠 2. UPDATE PRODUCT (ADMIN)
# =====================================================
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return await product_service.update_product(db, product_id, payload)


# =====================================================
# 🛠 3. DELETE PRODUCT (SOFT DELETE)
# =====================================================
@router.delete("/{product_id}", response_model=ProductDeleteResponse)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    await product_service.delete_product(db, product_id)
    return {"message": "Product deleted successfully"}


# =====================================================
# 🛠 4. RESTORE PRODUCT
# =====================================================
@router.patch("/{product_id}/restore", response_model=ProductResponse)
async def restore_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return await product_service.restore_product(db, product_id)


# =====================================================
# 🛠 5. PRODUCT STATS (ADMIN DASHBOARD)
# =====================================================
@router.get("/stats", response_model=ProductStatsResponse)
async def product_stats(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return await product_service.get_stats(db)