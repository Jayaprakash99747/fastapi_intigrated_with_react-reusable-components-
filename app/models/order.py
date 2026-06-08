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
)

from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.constants import OrderStatus


# ==========================================================
# ORDER
# ==========================================================

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer,primary_key=True,index=True)

    user_id = Column(Integer,ForeignKey("users.id",ondelete="RESTRICT",),nullable=False,index=True,)

    order_number = Column(String(50),unique=True,nullable=False,index=True,)

    status = Column(Enum(OrderStatus),default=OrderStatus.PENDING,nullable=False,)

    total_amount = Column(Float,nullable=False,)

    tax_amount = Column(Float,default=0,nullable=False,)

    discount_amount = Column(Float,default=0,nullable=False,)

    shipping_address = Column(Text,nullable=False,)

    tracking_number = Column(String(100),nullable=True,)

    notes = Column(Text,nullable=True,)

    created_at = Column(DateTime,default=datetime.utcnow,nullable=False,)

    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False,)

    # ======================================================
    # RELATIONSHIPS
    # ======================================================

    user = relationship("User",back_populates="orders",lazy="joined",)
    order_items = relationship("OrderItem",back_populates="order",cascade="all, delete-orphan",passive_deletes=True,)

    payment = relationship("Payment",back_populates="order",uselist=False,cascade="all, delete-orphan",)

    def __repr__(self):
        return (
            f"<Order("
            f"id={self.id}, "
            f"order_number='{self.order_number}', "
            f"status='{self.status.value}'"
            f")>"
        )


# ==========================================================
# ORDER ITEM
# ==========================================================

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer,primary_key=True,index=True,)

    order_id = Column(Integer,ForeignKey("orders.id",ondelete="CASCADE",),nullable=False,index=True,)

    product_id = Column(Integer,ForeignKey("products.id",ondelete="RESTRICT",),nullable=False,index=True,)

    quantity = Column(Integer,nullable=False,)

    unit_price = Column(Float,nullable=False,)

    discount_amount = Column(Float,default=0,nullable=False,)

    tax_amount = Column(Float,default=0,nullable=False,)

    created_at = Column(DateTime,default=datetime.utcnow,nullable=False,)

    # ======================================================
    # RELATIONSHIPS
    # ======================================================

    order = relationship("Order",back_populates="order_items",)

    product = relationship("Product",back_populates="order_items",lazy="joined",)

    @property
    def subtotal(self) -> float:
        """
        Quantity × Unit Price
        """
        return self.quantity * self.unit_price

    @property
    def total(self) -> float:
        """
        Final line item total
        """
        return (
            self.subtotal
            + self.tax_amount
            - self.discount_amount
        )

    def __repr__(self):
        return (
            f"<OrderItem("
            f"id={self.id}, "
            f"order_id={self.order_id}, "
            f"product_id={self.product_id}"
            f")>"
        )