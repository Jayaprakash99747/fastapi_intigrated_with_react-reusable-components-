from datetime import datetime
from uuid import uuid4
from typing import Optional

from sqlalchemy import (
    select,
    func,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    selectinload,
)

from app.models.order import (
    Order,
    OrderItem,
    OrderStatus,
)

from app.models.product import (
    Product,
)

from app.models.coupon import (
    Coupon,
)


class OrderCRUD:

    # =====================================================
    # GENERATE ORDER NUMBER
    # =====================================================

    async def generate_order_number(self) -> str:

        return f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{uuid4().hex[:8].upper()}"

    # =====================================================
    # CREATE ORDER
    # =====================================================

    async def create_order(
        self,
        db: AsyncSession,
        **kwargs,
    ) -> Order:

        order = Order(**kwargs)

        db.add(order)

        await db.commit()

        await db.refresh(order)

        return order

    # =====================================================
    # CREATE ORDER ITEM
    # =====================================================

    async def create_order_item(
        self,
        db: AsyncSession,
        **kwargs,
    ) -> OrderItem:

        item = OrderItem(**kwargs)

        db.add(item)

        await db.commit()

        await db.refresh(item)

        return item

    # =====================================================
    # GET ORDER
    # =====================================================

    async def get_order(
        self,
        db: AsyncSession,
        order_id: int,
    ) -> Optional[Order]:

        stmt = (
            select(Order)
            .options(
                selectinload(Order.order_items)
                .selectinload(OrderItem.product),

                selectinload(Order.payment),

                selectinload(Order.user),
            )
            .where(
                Order.id == order_id
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # GET ORDER BY NUMBER
    # =====================================================

    async def get_order_by_number(
        self,
        db: AsyncSession,
        order_number: str,
    ) -> Optional[Order]:

        stmt = (
            select(Order)
            .where(
                Order.order_number == order_number
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # USER ORDERS
    # =====================================================

    async def get_user_orders(
        self,
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
    ):

        stmt = (
            select(Order)
            .options(
                selectinload(Order.order_items),
                selectinload(Order.payment),
            )
            .where(
                Order.user_id == user_id
            )
            .order_by(
                Order.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # ALL ORDERS ADMIN
    # =====================================================

    async def get_orders(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50,
    ):

        stmt = (
            select(Order)
            .options(
                selectinload(Order.user),
                selectinload(Order.payment),
            )
            .order_by(
                Order.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # UPDATE STATUS
    # =====================================================

    async def update_status(
        self,
        db: AsyncSession,
        order: Order,
        status: OrderStatus,
    ) -> Order:

        order.status = status
        order.updated_at = datetime.utcnow()

        await db.commit()

        await db.refresh(order)

        return order

    # =====================================================
    # CANCEL ORDER
    # =====================================================

    async def cancel_order(
        self,
        db: AsyncSession,
        order: Order,
    ) -> Order:

        order.status = OrderStatus.CANCELLED
        order.updated_at = datetime.utcnow()

        await db.commit()

        await db.refresh(order)

        return order

    # =====================================================
    # ADD TRACKING NUMBER
    # =====================================================

    async def update_tracking(
        self,
        db: AsyncSession,
        order: Order,
        tracking_number: str,
    ) -> Order:

        order.tracking_number = tracking_number

        await db.commit()

        await db.refresh(order)

        return order

    # =====================================================
    # APPLY COUPON
    # =====================================================

    async def get_coupon(
        self,
        db: AsyncSession,
        code: str,
    ) -> Optional[Coupon]:

        stmt = (
            select(Coupon)
            .where(
                Coupon.code == code,
                Coupon.is_active.is_(True),
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # UPDATE COUPON USAGE
    # =====================================================

    async def increment_coupon_usage(
        self,
        db: AsyncSession,
        coupon: Coupon,
    ):

        coupon.current_uses += 1

        await db.commit()

    # =====================================================
    # PRODUCT
    # =====================================================

    async def get_product(
        self,
        db: AsyncSession,
        product_id: int,
    ) -> Optional[Product]:

        stmt = (
            select(Product)
            .where(
                Product.id == product_id,
                Product.is_deleted.is_(False),
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # REDUCE STOCK
    # =====================================================

    async def reduce_stock(
        self,
        db: AsyncSession,
        product: Product,
        quantity: int,
    ):

        product.stock_quantity -= quantity

        await db.commit()

    # =====================================================
    # RESTORE STOCK
    # =====================================================

    async def restore_stock(
        self,
        db: AsyncSession,
        product: Product,
        quantity: int,
    ):

        product.stock_quantity += quantity

        await db.commit()

    # =====================================================
    # ORDER COUNT
    # =====================================================

    async def order_count(
        self,
        db: AsyncSession,
    ) -> int:

        stmt = select(func.count(Order.id))

        result = await db.execute(stmt)

        return result.scalar() or 0

    # =====================================================
    # ORDER STATS
    # =====================================================

    async def order_stats(
        self,
        db: AsyncSession,
    ):

        total_orders = await db.scalar(
            select(func.count(Order.id))
        )

        pending_orders = await db.scalar(
            select(func.count(Order.id))
            .where(
                Order.status ==
                OrderStatus.PENDING
            )
        )

        delivered_orders = await db.scalar(
            select(func.count(Order.id))
            .where(
                Order.status ==
                OrderStatus.DELIVERED
            )
        )

        cancelled_orders = await db.scalar(
            select(func.count(Order.id))
            .where(
                Order.status ==
                OrderStatus.CANCELLED
            )
        )

        return {
            "total_orders": total_orders or 0,
            "pending_orders": pending_orders or 0,
            "delivered_orders": delivered_orders or 0,
            "cancelled_orders": cancelled_orders or 0,
        }

    # =====================================================
    # REVENUE STATS
    # =====================================================

    async def revenue_stats(
        self,
        db: AsyncSession,
    ):

        revenue = await db.scalar(
            select(
                func.sum(Order.total_amount)
            ).where(
                Order.status ==
                OrderStatus.DELIVERED
            )
        )

        return {
            "revenue": float(
                revenue or 0
            )
        }

    # =====================================================
    # ORDERS BY STATUS
    # =====================================================

    async def get_orders_by_status(
        self,
        db: AsyncSession,
        status: OrderStatus,
        skip: int = 0,
        limit: int = 20,
    ):

        stmt = (
            select(Order)
            .where(
                Order.status == status
            )
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # DELETE ORDER
    # =====================================================

    async def delete_order(
        self,
        db: AsyncSession,
        order: Order,
    ):

        await db.delete(order)

        await db.commit()

    async def get_user_cart_items(self, db, user_id):
        stmt = select(CartItem).where(CartItem.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalars().all()


    async def clear_cart(self, db, user_id):
        stmt = select(CartItem).where(CartItem.user_id == user_id)
        result = await db.execute(stmt)

        for item in result.scalars().all():
            await db.delete(item)

        await db.commit()    


order_crud = OrderCRUD()