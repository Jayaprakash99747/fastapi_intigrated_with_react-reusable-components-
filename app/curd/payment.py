from datetime import datetime
from typing import Optional

from sqlalchemy import (
    select,
    func,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    selectinload,
)

from app.models.payment import (
    Payment,
    PaymentStatus,
    PaymentProvider,
)

from app.models.order import (
    Order,
)


class PaymentCRUD:

    # =====================================================
    # CREATE PAYMENT
    # =====================================================

    async def create_payment(
        self,
        db: AsyncSession,
        **kwargs,
    ) -> Payment:

        payment = Payment(**kwargs)

        db.add(payment)

        await db.commit()

        await db.refresh(payment)

        return payment

    # =====================================================
    # GET PAYMENT
    # =====================================================

    async def get_payment(
        self,
        db: AsyncSession,
        payment_id: int,
    ) -> Optional[Payment]:

        stmt = (
            select(Payment)
            .options(
                selectinload(Payment.order)
            )
            .where(
                Payment.id == payment_id
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # GET BY ORDER
    # =====================================================

    async def get_by_order(
        self,
        db: AsyncSession,
        order_id: int,
    ) -> Optional[Payment]:

        stmt = (
            select(Payment)
            .where(
                Payment.order_id == order_id
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # GET BY PROVIDER ORDER ID
    # =====================================================

    async def get_by_provider_order_id(
        self,
        db: AsyncSession,
        provider_order_id: str,
    ) -> Optional[Payment]:

        stmt = (
            select(Payment)
            .where(
                Payment.provider_order_id ==
                provider_order_id
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # UPDATE STATUS
    # =====================================================

    async def update_status(
        self,
        db: AsyncSession,
        payment: Payment,
        status: PaymentStatus,
    ) -> Payment:

        payment.status = status
        payment.updated_at = datetime.utcnow()

        await db.commit()

        await db.refresh(payment)

        return payment

    # =====================================================
    # STORE SUCCESS RESPONSE
    # =====================================================

    async def mark_success(
        self,
        db: AsyncSession,
        payment: Payment,
        provider_payment_id: str,
        provider_signature: str | None = None,
    ) -> Payment:

        payment.status = PaymentStatus.SUCCESS
        payment.provider_payment_id = (
            provider_payment_id
        )

        payment.provider_signature = (
            provider_signature
        )

        payment.updated_at = datetime.utcnow()

        await db.commit()

        await db.refresh(payment)

        return payment

    # =====================================================
    # STORE FAILURE RESPONSE
    # =====================================================

    async def mark_failed(
        self,
        db: AsyncSession,
        payment: Payment,
        reason: str,
    ) -> Payment:

        payment.status = PaymentStatus.FAILED
        payment.failure_reason = reason
        payment.updated_at = datetime.utcnow()

        await db.commit()

        await db.refresh(payment)

        return payment

    # =====================================================
    # REFUND PAYMENT
    # =====================================================

    async def mark_refunded(
        self,
        db: AsyncSession,
        payment: Payment,
    ) -> Payment:

        payment.status = PaymentStatus.REFUNDED
        payment.updated_at = datetime.utcnow()

        await db.commit()

        await db.refresh(payment)

        return payment

    # =====================================================
    # VERIFY PAYMENT
    # =====================================================

    async def verify_payment(
        self,
        db: AsyncSession,
        payment_id: int,
    ) -> bool:

        payment = await self.get_payment(
            db,
            payment_id,
        )

        if not payment:
            return False

        return (
            payment.status
            == PaymentStatus.SUCCESS
        )

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
            .where(
                Order.id == order_id
            )
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # PAYMENT EXISTS
    # =====================================================

    async def payment_exists(
        self,
        db: AsyncSession,
        order_id: int,
    ) -> bool:

        stmt = (
            select(Payment.id)
            .where(
                Payment.order_id == order_id
            )
        )

        result = await db.execute(stmt)

        return (
            result.scalar_one_or_none()
            is not None
        )

    # =====================================================
    # PAYMENT COUNT
    # =====================================================

    async def payment_count(
        self,
        db: AsyncSession,
    ) -> int:

        stmt = (
            select(
                func.count(Payment.id)
            )
        )

        result = await db.execute(stmt)

        return result.scalar() or 0

    # =====================================================
    # PAYMENT STATS
    # =====================================================

    async def payment_stats(
        self,
        db: AsyncSession,
    ):

        total = await db.scalar(
            select(func.count(Payment.id))
        )

        success = await db.scalar(
            select(func.count(Payment.id))
            .where(
                Payment.status ==
                PaymentStatus.SUCCESS
            )
        )

        pending = await db.scalar(
            select(func.count(Payment.id))
            .where(
                Payment.status ==
                PaymentStatus.PENDING
            )
        )

        failed = await db.scalar(
            select(func.count(Payment.id))
            .where(
                Payment.status ==
                PaymentStatus.FAILED
            )
        )

        refunded = await db.scalar(
            select(func.count(Payment.id))
            .where(
                Payment.status ==
                PaymentStatus.REFUNDED
            )
        )

        return {
            "total_payments": total or 0,
            "success": success or 0,
            "pending": pending or 0,
            "failed": failed or 0,
            "refunded": refunded or 0,
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
                func.sum(Payment.amount)
            )
            .where(
                Payment.status ==
                PaymentStatus.SUCCESS
            )
        )

        return {
            "total_revenue": float(
                revenue or 0
            )
        }

    # =====================================================
    # PAYMENTS BY PROVIDER
    # =====================================================

    async def payments_by_provider(
        self,
        db: AsyncSession,
        provider: PaymentProvider,
        skip: int = 0,
        limit: int = 20,
    ):

        stmt = (
            select(Payment)
            .where(
                Payment.provider == provider
            )
            .offset(skip)
            .limit(limit)
            .order_by(
                Payment.created_at.desc()
            )
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # LIST PAYMENTS
    # =====================================================

    async def get_payments(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50,
    ):

        stmt = (
            select(Payment)
            .options(
                selectinload(Payment.order)
            )
            .order_by(
                Payment.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(stmt)

        return result.scalars().all()

    # =====================================================
    # DELETE PAYMENT
    # =====================================================

    async def delete_payment(
        self,
        db: AsyncSession,
        payment: Payment,
    ):

        await db.delete(payment)

        await db.commit()


payment_crud = PaymentCRUD()