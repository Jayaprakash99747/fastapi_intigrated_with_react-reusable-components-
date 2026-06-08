# import razorpay
# from app.core.config import settings

# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# async def create_razorpay_order(amount: int, currency: str = "INR"):
#     data = {
#         "amount": int(amount * 100),  # paise
#         "currency": currency,
#         "payment_capture": "1"
#     }
#     return client.order.create(data)












from datetime import datetime
from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import (
    Payment,
    PaymentStatus,
    PaymentProvider,
)

from app.models.order import Order
from app.curd.payment import payment_crud
from app.core.logging_configuration import settings


# NOTE:
# In production, these SDKs would be installed:
# pip install razorpay stripe


class PaymentService:

    # =====================================================
    # CREATE PAYMENT INIT (ORDER LEVEL)
    # =====================================================

    async def create_payment_order(
        self,
        db: AsyncSession,
        order: Order,
        provider: PaymentProvider,
    ) -> Payment:

        payment = await payment_crud.create_payment(
            db,
            order_id=order.id,
            provider=provider,
            amount=order.total_amount,
            currency="INR",
            status=PaymentStatus.PENDING,
        )

        return payment

    # =====================================================
    # RAZORPAY ORDER CREATE (SIMULATED STRUCTURE)
    # =====================================================

    async def create_razorpay_order(
        self,
        payment: Payment,
    ) -> dict:

        # In real project:
        # import razorpay
        # client = razorpay.Client(auth=(key_id, key_secret))

        return {
            "id": f"order_{payment.id}",
            "amount": int(payment.amount * 100),
            "currency": "INR",
            "status": "created",
            "payment_id": payment.id,
        }

    # =====================================================
    # STRIPE PAYMENT INTENT (SIMULATED)
    # =====================================================

    async def create_stripe_payment(
        self,
        payment: Payment,
    ) -> dict:

        return {
            "id": f"pi_{payment.id}",
            "amount": int(payment.amount * 100),
            "currency": "inr",
            "status": "requires_payment_method",
            "client_secret": f"secret_{payment.id}",
        }

    # =====================================================
    # VERIFY RAZORPAY PAYMENT
    # =====================================================

    async def verify_razorpay_payment(
        self,
        db: AsyncSession,
        payment_id: int,
        provider_payment_id: str,
        signature: str,
    ) -> bool:

        payment = await payment_crud.get_payment(db, payment_id)

        if not payment:
            return False

        # In real Razorpay:
        # verify_signature(order_id, payment_id, signature)

        is_valid = True  # simulated

        if is_valid:
            await payment_crud.mark_success(
                db,
                payment,
                provider_payment_id,
                provider_signature=signature,
            )

            return True

        await payment_crud.mark_failed(
            db,
            payment,
            reason="Invalid signature",
        )

        return False

    # =====================================================
    # VERIFY STRIPE PAYMENT
    # =====================================================

    async def verify_stripe_payment(
        self,
        db: AsyncSession,
        payment_id: int,
        stripe_payment_intent: str,
    ) -> bool:

        payment = await payment_crud.get_payment(db, payment_id)

        if not payment:
            return False

        # In real Stripe:
        # stripe.PaymentIntent.retrieve(...)

        success = True  # simulated

        if success:
            await payment_crud.mark_success(
                db,
                payment,
                provider_payment_id=stripe_payment_intent,
            )
            return True

        await payment_crud.mark_failed(
            db,
            payment,
            reason="Stripe payment failed",
        )

        return False

    # =====================================================
    # COD PAYMENT (CASH ON DELIVERY)
    # =====================================================

    async def create_cod_payment(
        self,
        db: AsyncSession,
        order: Order,
    ) -> Payment:

        payment = await payment_crud.create_payment(
            db,
            order_id=order.id,
            provider=PaymentProvider.COD,
            amount=order.total_amount,
            currency="INR",
            status=PaymentStatus.PENDING,
        )

        # COD is auto-marked success on delivery in real systems
        return payment

    # =====================================================
    # WEBHOOK HANDLER (GENERIC)
    # =====================================================

    async def handle_webhook(
        self,
        db: AsyncSession,
        provider: PaymentProvider,
        payload: dict,
    ) -> bool:

        if provider == PaymentProvider.RAZORPAY:

            payment_id = payload.get("payment_id")
            signature = payload.get("signature")

            return await self.verify_razorpay_payment(
                db,
                payment_id,
                payload.get("provider_payment_id"),
                signature,
            )

        if provider == PaymentProvider.STRIPE:

            return await self.verify_stripe_payment(
                db,
                payload.get("payment_id"),
                payload.get("stripe_payment_intent"),
            )

        return False

    # =====================================================
    # REFUND PAYMENT
    # =====================================================

    async def refund_payment(
        self,
        db: AsyncSession,
        payment_id: int,
    ) -> bool:

        payment = await payment_crud.get_payment(db, payment_id)

        if not payment:
            return False

        # In real system:
        # call Razorpay/Stripe refund API here

        await payment_crud.mark_refunded(db, payment)

        return True

    # =====================================================
    # PAYMENT STATUS CHECK
    # =====================================================

    async def get_payment_status(
        self,
        db: AsyncSession,
        payment_id: int,
    ) -> Optional[str]:

        payment = await payment_crud.get_payment(db, payment_id)

        if not payment:
            return None

        return payment.status.value

    # =====================================================
    # PAYMENT SUMMARY
    # =====================================================

    async def payment_summary(
        self,
        db: AsyncSession,
    ):

        stats = await payment_crud.payment_stats(db)
        revenue = await payment_crud.revenue_stats(db)

        return {
            "stats": stats,
            "revenue": revenue,
        }


payment_service = PaymentService()