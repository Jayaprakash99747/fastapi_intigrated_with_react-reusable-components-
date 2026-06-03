from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    ForeignKey,
    Enum,
    Boolean,
)

from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.constants import (
    PaymentStatus,
    PaymentProvider,
)


# ==========================================================
# PAYMENT
# ==========================================================

class Payment(Base):
    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    order_id = Column(
        Integer,
        ForeignKey(
            "orders.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    provider = Column(
        Enum(PaymentProvider),
        nullable=False,
    )

    amount = Column(
        Float,
        nullable=False,
    )

    currency = Column(
        String(10),
        default="INR",
        nullable=False,
    )

    status = Column(
        Enum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False,
    )

    # ======================================================
    # RAZORPAY
    # ======================================================

    provider_order_id = Column(
        String(255),
        nullable=True,
        index=True,
    )

    provider_payment_id = Column(
        String(255),
        nullable=True,
        index=True,
    )

    provider_signature = Column(
        String(1000),
        nullable=True,
    )

    # ======================================================
    # STRIPE
    # ======================================================

    stripe_payment_intent_id = Column(
        String(255),
        nullable=True,
        index=True,
    )

    stripe_customer_id = Column(
        String(255),
        nullable=True,
    )

    stripe_charge_id = Column(
        String(255),
        nullable=True,
    )

    # ======================================================
    # REFUND
    # ======================================================

    refund_id = Column(
        String(255),
        nullable=True,
        index=True,
    )

    refunded_amount = Column(
        Float,
        default=0,
        nullable=False,
    )

    refund_reason = Column(
        Text,
        nullable=True,
    )

    refunded_at = Column(
        DateTime,
        nullable=True,
    )

    # ======================================================
    # FAILURE
    # ======================================================

    failure_reason = Column(
        Text,
        nullable=True,
    )

    # ======================================================
    # WEBHOOK
    # ======================================================

    webhook_received = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    webhook_payload = Column(
        Text,
        nullable=True,
    )

    # ======================================================
    # AUDIT
    # ======================================================

    paid_at = Column(
        DateTime,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # ======================================================
    # RELATIONSHIP
    # ======================================================

    order = relationship(
        "Order",
        back_populates="payment",
        lazy="joined",
    )

    # ======================================================
    # HELPERS
    # ======================================================

    @property
    def is_paid(self) -> bool:
        return self.status == PaymentStatus.SUCCESS

    @property
    def is_failed(self) -> bool:
        return self.status == PaymentStatus.FAILED

    @property
    def is_refunded(self) -> bool:
        return self.status == PaymentStatus.REFUNDED

    @property
    def can_refund(self) -> bool:
        return self.status == PaymentStatus.SUCCESS

    def __repr__(self):
        return (
            f"<Payment("
            f"id={self.id}, "
            f"order_id={self.order_id}, "
            f"provider='{self.provider.value}', "
            f"status='{self.status.value}'"
            f")>"
        )