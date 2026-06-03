from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    CheckConstraint,
)

from app.core.database import Base


# ==========================================================
# COUPON
# ==========================================================

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    code = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    discount_percent = Column(
        Float,
        nullable=False,
    )

    max_uses = Column(
        Integer,
        default=100,
        nullable=False,
    )

    current_uses = Column(
        Integer,
        default=0,
        nullable=False,
    )

    min_order_amount = Column(
        Float,
        default=0,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    expiry_date = Column(
        DateTime,
        nullable=False,
        index=True,
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
    # DATABASE CONSTRAINTS
    # ======================================================

    __table_args__ = (

        CheckConstraint(
            "discount_percent >= 0",
            name="ck_coupon_discount_positive",
        ),

        CheckConstraint(
            "discount_percent <= 100",
            name="ck_coupon_discount_max",
        ),

        CheckConstraint(
            "max_uses >= 0",
            name="ck_coupon_max_uses_positive",
        ),

        CheckConstraint(
            "current_uses >= 0",
            name="ck_coupon_current_uses_positive",
        ),

        CheckConstraint(
            "min_order_amount >= 0",
            name="ck_coupon_min_order_amount_positive",
        ),
    )

    # ======================================================
    # HELPER PROPERTIES
    # ======================================================

    @property
    def is_expired(self) -> bool:
        """
        Check if coupon is expired.
        """
        return datetime.utcnow() > self.expiry_date

    @property
    def remaining_uses(self) -> int:
        """
        Remaining coupon usage count.
        """
        return max(
            self.max_uses - self.current_uses,
            0,
        )

    @property
    def is_usage_limit_reached(self) -> bool:
        """
        Has coupon reached max usage?
        """
        return self.current_uses >= self.max_uses

    @property
    def can_use(self) -> bool:
        """
        Coupon can currently be used.
        """
        return (
            self.is_active
            and not self.is_expired
            and not self.is_usage_limit_reached
        )

    # ======================================================
    # BUSINESS METHODS
    # ======================================================

    def validate_order_amount(
        self,
        order_amount: float,
    ) -> bool:
        """
        Validate minimum order amount.
        """

        return (
            order_amount >= self.min_order_amount
        )

    def calculate_discount(
        self,
        order_amount: float,
    ) -> float:
        """
        Calculate discount value.
        """

        if not self.can_use:
            return 0

        if not self.validate_order_amount(
            order_amount
        ):
            return 0

        return round(
            (
                order_amount
                * self.discount_percent
            ) / 100,
            2,
        )

    def increment_usage(self):
        """
        Increase coupon usage count.
        """

        self.current_uses += 1

    # ======================================================
    # REPR
    # ======================================================

    def __repr__(self):

        return (
            f"<Coupon("
            f"id={self.id}, "
            f"code='{self.code}', "
            f"discount={self.discount_percent}%"
            f")>"
        )