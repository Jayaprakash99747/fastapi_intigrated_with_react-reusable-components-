from typing import Optional

from sqlalchemy import (
    select,
    func,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    selectinload,
)

from app.models.product import (
    Product,
    CartItem,
)


class CartCRUD:

    # =====================================================
    # ADD TO CART
    # =====================================================

    async def add_to_cart(
        self,
        db: AsyncSession,
        user_id: int,
        product_id: int,
        quantity: int = 1,
    ) -> CartItem:

        stmt = (
            select(CartItem)
            .where(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id,
            )
        )

        result = await db.execute(stmt)

        cart_item = result.scalar_one_or_none()

        if cart_item:
            cart_item.quantity += quantity

            await db.commit()

            await db.refresh(cart_item)

            return cart_item

        cart_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
        )

        db.add(cart_item)

        await db.commit()

        await db.refresh(cart_item)

        return cart_item

    # =====================================================
    # GET USER CART
    # =====================================================

    async def get_cart(
        self,
        db: AsyncSession,
        user_id: int,
    ):

        stmt = (
            select(CartItem)
            .options(
                selectinload(CartItem.product)
                .selectinload(Product.images)
            )
            .where(
                CartItem.user_id == user_id
            )
            .order_by(
                CartItem.created_at.desc()
            )
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # GET CART ITEM
    # =====================================================

    async def get_cart_item(
        self,
        db: AsyncSession,
        cart_item_id: int,
        user_id: int,
    ) -> Optional[CartItem]:

        stmt = (
            select(CartItem)
            .options(
                selectinload(CartItem.product)
            )
            .where(
                CartItem.id == cart_item_id,
                CartItem.user_id == user_id,
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # UPDATE QUANTITY
    # =====================================================

    async def update_quantity(
        self,
        db: AsyncSession,
        cart_item: CartItem,
        quantity: int,
    ) -> CartItem:

        cart_item.quantity = quantity

        await db.commit()

        await db.refresh(cart_item)

        return cart_item

    # =====================================================
    # REMOVE ITEM
    # =====================================================

    async def remove_item(
        self,
        db: AsyncSession,
        cart_item: CartItem,
    ) -> None:

        await db.delete(cart_item)

        await db.commit()

    # =====================================================
    # CLEAR CART
    # =====================================================

    async def clear_cart(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> None:

        stmt = (
            select(CartItem)
            .where(
                CartItem.user_id == user_id
            )
        )

        result = await db.execute(stmt)

        items = result.scalars().all()

        for item in items:
            await db.delete(item)

        await db.commit()

    # =====================================================
    # PRODUCT EXISTS
    # =====================================================

    async def product_exists(
        self,
        db: AsyncSession,
        product_id: int,
    ) -> bool:

        stmt = (
            select(Product.id)
            .where(
                Product.id == product_id,
                Product.is_deleted.is_(False),
                Product.is_available.is_(True),
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none() is not None

    # =====================================================
    # GET PRODUCT
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
    # CART COUNT
    # =====================================================

    async def cart_count(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> int:

        stmt = (
            select(
                func.count(CartItem.id)
            )
            .where(
                CartItem.user_id == user_id
            )
        )

        result = await db.execute(stmt)

        return result.scalar() or 0

    # =====================================================
    # CART SUMMARY
    # =====================================================

    async def cart_summary(
        self,
        db: AsyncSession,
        user_id: int,
    ):

        cart_items = await self.get_cart(
            db=db,
            user_id=user_id,
        )

        subtotal = 0
        total_discount = 0
        total_tax = 0

        items = []

        for item in cart_items:

            product = item.product

            item_price = product.price

            quantity = item.quantity

            discount = (
                item_price *
                (product.discount_percent / 100)
            )

            final_price = item_price - discount

            tax = (
                final_price *
                (product.gst_percent / 100)
            )

            line_total = (
                (final_price + tax)
                * quantity
            )

            subtotal += line_total
            total_discount += discount * quantity
            total_tax += tax * quantity

            items.append(
                {
                    "product_id": product.id,
                    "name": product.name,
                    "quantity": quantity,
                    "unit_price": item_price,
                    "line_total": round(
                        line_total,
                        2,
                    ),
                }
            )

        return {
            "items": items,
            "subtotal": round(
                subtotal,
                2,
            ),
            "discount": round(
                total_discount,
                2,
            ),
            "tax": round(
                total_tax,
                2,
            ),
            "grand_total": round(
                subtotal,
                2,
            ),
        }

    # =====================================================
    # VALIDATE CHECKOUT
    # =====================================================

    async def validate_checkout(
        self,
        db: AsyncSession,
        user_id: int,
    ):

        cart_items = await self.get_cart(
            db,
            user_id,
        )

        if not cart_items:
            return False, "Cart is empty"

        for item in cart_items:

            product = item.product

            if not product.is_available:
                return (
                    False,
                    f"{product.name} unavailable",
                )

            if (
                product.stock_quantity
                < item.quantity
            ):
                return (
                    False,
                    f"Insufficient stock for {product.name}",
                )

        return True, "Checkout valid"
    
    
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


cart_crud = CartCRUD()