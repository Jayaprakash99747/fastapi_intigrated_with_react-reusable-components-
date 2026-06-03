from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderItem, OrderStatus
from app.models.cart import CartItem
from app.models.payment import PaymentProvider

from app.curd.order import order_crud
from app.curd.inventory import inventory_crud
from app.curd.coupon import coupon_crud

from app.services.payment_service import payment_service
from app.services.email_service import email_service
from app.websocket.notification import manager
from app.api.dependencies import get_current_user,get_admin_user


class OrderService:

    # =====================================================
    # CREATE ORDER (FULL FLOW)
    # =====================================================
    async def create_order(
        self,
        db: AsyncSession,
        user_id: int,
        shipping_address: str,
        coupon_code: str | None = None,
        payment_provider: PaymentProvider = PaymentProvider.RAZORPAY,
    ):

        # 1. GET CART
        cart_items = await order_crud.get_user_cart_items(db, user_id)

        if not cart_items:
            raise ValueError("Cart is empty")

        # 2. STOCK VALIDATION
        for item in cart_items:
            product = await order_crud.get_product(db, item.product_id)

            if product.stock_quantity < item.quantity:
                raise ValueError(f"Insufficient stock for {product.name}")

        # 3. CALCULATE TOTAL
        total = sum(item.product.price * item.quantity for item in cart_items)

        discount = 0

        # 4. APPLY COUPON
        if coupon_code:
            coupon = await order_crud.get_coupon(db, coupon_code)

            if coupon:
                discount = (total * coupon.discount_percent) / 100
                await order_crud.increment_coupon_usage(db, coupon)

        final_total = total - discount

        # 5. CREATE ORDER
        order = await order_crud.create_order(
            db,
            user_id=user_id,
            order_number=await order_crud.generate_order_number(),
            status=OrderStatus.PENDING,
            total_amount=final_total,
            shipping_address=shipping_address,
            discount_amount=discount,
        )

        # 6. CREATE ORDER ITEMS
        for item in cart_items:
            await order_crud.create_order_item(
                db,
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.product.price,
            )

        # 7. DEDUCT STOCK
        for item in cart_items:
            await inventory_crud.stock_out(
                db,
                item.product_id,
                item.quantity,
            )

        # 8. CLEAR CART
        await order_crud.clear_cart(db, user_id)

        # 9. CREATE PAYMENT
        payment = await payment_service.create_payment_order(
            db,
            order,
            provider=payment_provider,
        )

        # 10. REAL-TIME NOTIFICATION (ADMIN)
        await manager.send_to_channel(
            "admin",
            {
                "type": "NEW_ORDER",
                "order_id": order.id,
                "order_number": order.order_number,
                "amount": final_total,
            },
        )

        # 11. REAL-TIME NOTIFICATION (USER)
        await manager.send_to_channel(
            "user",
            {
                "type": "ORDER_PLACED",
                "order_id": order.id,
                "status": "PENDING",
            },
        )

        # 12. EMAIL TO USER
        await email_service.send_email(
            subject="Order Placed Successfully",
            email=order.user.email,
            body=f"""
                <h2>Your Order is Confirmed</h2>
                <p>Order ID: {order.order_number}</p>
                <p>Total: {final_total}</p>
            """,
        )

        # 13. EMAIL TO ADMIN
        await email_service.send_email(
            subject="New Order Received",
            email="admin@example.com",
            body=f"""
                <h2>New Order Alert</h2>
                <p>Order: {order.order_number}</p>
                <p>Amount: {final_total}</p>
            """,
        )

        return order

# -------------------------------------------------------------------------
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.order_service import order_service
from app.services.auth_service import AuthService

from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderListResponse,
    OrderDetailResponse,
    OrderCancelRequest,
    OrderStatusUpdate,
    OrderSummaryResponse,
)

router = APIRouter(prefix="/orders", tags=["Orders"])


# =====================================================
# 👤 CUSTOMER ENDPOINTS
# =====================================================

# 1. CREATE ORDER (CHECKOUT)
@router.post("/", response_model=OrderResponse)
async def create_order(
    payload: OrderCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await order_service.create_order(
        db=db,
        user_id=user.id,
        shipping_address=payload.shipping_address,
        coupon_code=payload.coupon_code,
    )


# 2. GET MY ORDERS
@router.get("/me", response_model=OrderListResponse)
async def my_orders(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
):
    items = await order_service.get_user_orders(
        db, user.id, skip, limit
    )
    return {"items": items}


# 3. GET ORDER DETAILS
@router.get("/{order_id}", response_model=OrderDetailResponse)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await order_service.get_order(db, order_id)


# 4. CANCEL ORDER (CUSTOMER)
@router.patch("/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    payload: OrderCancelRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await order_service.cancel_order(
        db=db,
        order_id=order_id,
        user_id=user.id,
        reason=payload.reason,
    )


# =====================================================
# 🛠 ADMIN ENDPOINTS
# =====================================================

# 5. GET ALL ORDERS (ADMIN)
@router.get("/admin/all", response_model=OrderListResponse)
async def all_orders(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
    skip: int = 0,
    limit: int = 50,
):
    items = await order_service.get_all_orders(
        db, skip, limit
    )
    return {"items": items}


# 6. GET ORDERS BY STATUS (ADMIN)
@router.get("/admin/status/{status}")
async def orders_by_status(
    status: str,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return await order_service.get_orders_by_status(db, status)


# 7. UPDATE ORDER STATUS (ADMIN)
@router.patch("/admin/{order_id}/status")
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


# 8. UPDATE TRACKING NUMBER (ADMIN)
@router.patch("/admin/{order_id}/tracking")
async def update_tracking(
    order_id: int,
    tracking_number: str,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return await order_service.update_tracking(
        db, order_id, tracking_number
    )


# 9. ORDER SUMMARY DASHBOARD (ADMIN)
@router.get("/admin/summary", response_model=OrderSummaryResponse)
async def summary(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return await order_service.order_summary(db)


# 10. DELETE ORDER (ADMIN)
@router.delete("/admin/{order_id}")
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return await order_service.delete_order(db, order_id)


# =====================================================
# 💳 PAYMENT ENDPOINTS
# =====================================================

# 11. INITIATE PAYMENT FOR ORDER
@router.post("/{order_id}/payment/initiate")
async def initiate_payment(
    order_id: int,
    provider: str = "razorpay",
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await order_service.initiate_payment(
        db=db,
        order_id=order_id,
        provider=provider,
    )


# 12. VERIFY PAYMENT (RAZORPAY / STRIPE)
@router.post("/payment/verify")
async def verify_payment(
    payment_id: int,
    provider_payment_id: str,
    signature: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await order_service.verify_payment(
        db=db,
        payment_id=payment_id,
        provider_payment_id=provider_payment_id,
        signature=signature,
    )


# 13. PAYMENT STATUS CHECK
@router.get("/payment/{payment_id}/status")
async def payment_status(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await order_service.get_payment_status(db, payment_id)







