from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.order import Order, OrderItem, OrderStatus
from app.models.cart import CartItem
from app.models.product import Product
from app.models.inventory import Inventory

from app.curd.order import order_crud
from app.curd.inventory import inventory_crud
from app.services.payment_service import payment_service
from app.models.payment import PaymentProvider, PaymentStatus


class OrderService:

    # =====================================================
    # CALCULATE CART TOTAL
    # =====================================================

    async def calculate_cart_total(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> Tuple[float, List[CartItem]]:

        stmt = select(CartItem).where(CartItem.user_id == user_id)
        result = await db.execute(stmt)
        cart_items = result.scalars().all()

        total = 0.0

        for item in cart_items:
            product = item.product
            total += product.price * item.quantity

        return total, cart_items

    # =====================================================
    # CHECK STOCK BEFORE ORDER
    # =====================================================

    async def validate_stock(
        self,
        db: AsyncSession,
        cart_items: List[CartItem],
    ) -> Tuple[bool, str]:

        for item in cart_items:
            inventory = await inventory_crud.get_by_product(
                db,
                item.product_id,
            )

            if not inventory:
                return False, f"Inventory missing for product {item.product_id}"

            if inventory.available_stock < item.quantity:
                return False, f"Insufficient stock for product {item.product_id}"

        return True, "Stock available"

    # =====================================================
    # CREATE ORDER (MAIN CHECKOUT FLOW)
    # =====================================================

    async def create_order(
        self,
        db: AsyncSession,
        user_id: int,
        shipping_address: str,
        payment_provider: PaymentProvider = PaymentProvider.RAZORPAY,
    ) -> Optional[Order]:

        # 1. Get cart
        total, cart_items = await self.calculate_cart_total(db, user_id)

        if not cart_items:
            return None

        # 2. Validate stock
        valid, message = await self.validate_stock(db, cart_items)

        if not valid:
            raise ValueError(message)

        # 3. Create order
        order = await order_crud.create_order(
            db,
            user_id=user_id,
            order_number=f"ORD-{int(datetime.utcnow().timestamp())}",
            status=OrderStatus.PENDING,
            total_amount=total,
            shipping_address=shipping_address,
        )

        # 4. Create order items
        for item in cart_items:

            product = item.product

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
                discount_amount=0,
                tax_amount=0,
            )

            db.add(order_item)

        await db.commit()

        # 5. Deduct inventory
        for item in cart_items:
            await inventory_crud.stock_out(
                db,
                item.product_id,
                item.quantity,
            )

        # 6. Clear cart
        for item in cart_items:
            await db.delete(item)

        await db.commit()

        # 7. Create payment
        await payment_service.create_payment_order(
            db,
            order,
            provider=payment_provider,
        )

        return order

    # =====================================================
    # GET USER ORDERS
    # =====================================================

    async def get_user_orders(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> List[Order]:

        return await order_crud.get_user_orders(db, user_id)

    # =====================================================
    # GET ORDER BY ID
    # =====================================================

    async def get_order(
        self,
        db: AsyncSession,
        order_id: int,
    ) -> Optional[Order]:

        return await order_crud.get_order(db, order_id)

    # =====================================================
    # CANCEL ORDER
    # =====================================================

    async def cancel_order(
        self,
        db: AsyncSession,
        order_id: int,
    ) -> Optional[Order]:

        order = await order_crud.get_order(db, order_id)

        if not order:
            return None

        if order.status in [
            OrderStatus.SHIPPED,
            OrderStatus.DELIVERED,
        ]:
            raise ValueError("Cannot cancel shipped/delivered order")

        order.status = OrderStatus.CANCELLED

        # restore inventory
        for item in order.order_items:
            await inventory_crud.stock_in(
                db,
                item.product_id,
                item.quantity,
            )

        await db.commit()

        return order

    # =====================================================
    # UPDATE ORDER STATUS
    # =====================================================

    async def update_status(
        self,
        db: AsyncSession,
        order_id: int,
        status: OrderStatus,
    ) -> Optional[Order]:

        order = await order_crud.get_order(db, order_id)

        if not order:
            return None

        order.status = status

        await db.commit()
        await db.refresh(order)

        return order

    # =====================================================
    # ORDER SUMMARY
    # =====================================================

    async def order_summary(
        self,
        db: AsyncSession,
        user_id: int,
    ):

        orders = await order_crud.get_user_orders(db, user_id)

        total_orders = len(orders)
        total_spent = sum(o.total_amount for o in orders)

        return {
            "total_orders": total_orders,
            "total_spent": total_spent,
        }


order_service = OrderService()