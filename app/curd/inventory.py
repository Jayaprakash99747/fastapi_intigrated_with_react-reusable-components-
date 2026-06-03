from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.models.inventory import Inventory


class InventoryCRUD:

    # =====================================================
    # GET INVENTORY BY PRODUCT
    # =====================================================

    async def get_by_product(
        self,
        db: AsyncSession,
        product_id: int,
    ) -> Optional[Inventory]:

        stmt = select(Inventory).where(
            Inventory.product_id == product_id
        )

        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    # =====================================================
    # CREATE INVENTORY RECORD
    # =====================================================

    async def create_inventory(
        self,
        db: AsyncSession,
        product_id: int,
        stock_in: int = 0,
        reorder_level: int = 10,
    ) -> Inventory:

        inventory = Inventory(
            product_id=product_id,
            stock_in=stock_in,
            stock_out=0,
            available_stock=stock_in,
            reorder_level=reorder_level,
        )

        db.add(inventory)
        await db.commit()
        await db.refresh(inventory)

        return inventory

    # =====================================================
    # STOCK IN (ADD STOCK)
    # =====================================================

    async def stock_in(
        self,
        db: AsyncSession,
        product_id: int,
        quantity: int,
    ) -> Inventory:

        inventory = await self.get_by_product(db, product_id)

        if not inventory:
            inventory = await self.create_inventory(
                db,
                product_id=product_id,
                stock_in=quantity,
            )
            return inventory

        inventory.stock_in += quantity
        inventory.available_stock += quantity

        await db.commit()
        await db.refresh(inventory)

        return inventory

    # =====================================================
    # STOCK OUT (SALES / ORDER)
    # =====================================================

    async def stock_out(
        self,
        db: AsyncSession,
        product_id: int,
        quantity: int,
    ) -> Inventory:

        inventory = await self.get_by_product(db, product_id)

        if not inventory:
            raise ValueError("Inventory record not found")

        if inventory.available_stock < quantity:
            raise ValueError("Insufficient stock")

        inventory.stock_out += quantity
        inventory.available_stock -= quantity

        await db.commit()
        await db.refresh(inventory)

        return inventory

    # =====================================================
    # SYNC PRODUCT STOCK
    # =====================================================

    async def sync_product_stock(
        self,
        db: AsyncSession,
        product_id: int,
    ) -> Optional[Product]:

        inventory = await self.get_by_product(db, product_id)

        if not inventory:
            return None

        stmt = select(Product).where(Product.id == product_id)
        result = await db.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            return None

        product.stock_quantity = inventory.available_stock

        await db.commit()
        await db.refresh(product)

        return product

    # =====================================================
    # LOW STOCK PRODUCTS
    # =====================================================

    async def low_stock_items(
        self,
        db: AsyncSession,
        limit: int = 10,
    ) -> List[Inventory]:

        stmt = (
            select(Inventory)
            .where(
                Inventory.available_stock
                <= Inventory.reorder_level
            )
            .limit(limit)
        )

        result = await db.execute(stmt)
        return result.scalars().all()

    # =====================================================
    # OUT OF STOCK PRODUCTS
    # =====================================================

    async def out_of_stock(
        self,
        db: AsyncSession,
    ) -> List[Inventory]:

        stmt = select(Inventory).where(
            Inventory.available_stock == 0
        )

        result = await db.execute(stmt)
        return result.scalars().all()

    # =====================================================
    # INVENTORY SUMMARY
    # =====================================================

    async def inventory_summary(
        self,
        db: AsyncSession,
    ):

        total_items = await db.scalar(
            select(func.count(Inventory.id))
        )

        total_stock = await db.scalar(
            select(func.sum(Inventory.available_stock))
        )

        low_stock = await db.scalar(
            select(func.count(Inventory.id)).where(
                Inventory.available_stock
                <= Inventory.reorder_level
            )
        )

        out_of_stock = await db.scalar(
            select(func.count(Inventory.id)).where(
                Inventory.available_stock == 0
            )
        )

        return {
            "total_items": total_items or 0,
            "total_stock": total_stock or 0,
            "low_stock_items": low_stock or 0,
            "out_of_stock_items": out_of_stock or 0,
        }

    # =====================================================
    # DELETE INVENTORY
    # =====================================================

    async def delete_inventory(
        self,
        db: AsyncSession,
        inventory: Inventory,
    ) -> None:

        await db.delete(inventory)
        await db.commit()

    # =====================================================
    # RESET INVENTORY
    # =====================================================

    async def reset_inventory(
        self,
        db: AsyncSession,
        product_id: int,
    ) -> Optional[Inventory]:

        inventory = await self.get_by_product(db, product_id)

        if not inventory:
            return None

        inventory.stock_in = 0
        inventory.stock_out = 0
        inventory.available_stock = 0

        await db.commit()
        await db.refresh(inventory)

        return inventory

    # =====================================================
    # CHECK STOCK AVAILABILITY
    # =====================================================

    async def is_available(
        self,
        db: AsyncSession,
        product_id: int,
        quantity: int,
    ) -> bool:

        inventory = await self.get_by_product(db, product_id)

        if not inventory:
            return False

        return inventory.available_stock >= quantity


inventory_crud = InventoryCRUD()