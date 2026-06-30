from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    CheckConstraint,
)

from sqlalchemy.orm import relationship

from app.core.database import Base


# ==========================================================
# INVENTORY
# ==========================================================

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer,primary_key=True,index=True,)

    product_id = Column(Integer,ForeignKey("products.id",ondelete="CASCADE",),nullable=False,unique=True,index=True,)

    stock_in = Column(Integer,default=0,nullable=False,)

    stock_out = Column(Integer,default=0,nullable=False,)

    available_stock = Column(Integer,default=0,nullable=False,)

    reorder_level = Column(Integer,default=10,nullable=False,)

    last_updated = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False,)

    created_at = Column(DateTime,default=datetime.utcnow,nullable=False,)

    # ======================================================
    # RELATIONSHIP
    # ======================================================

    product = relationship("Product",back_populates="inventory",lazy="joined",)

    # ======================================================
    # CONSTRAINTS
    # ======================================================

    __table_args__ = (

        CheckConstraint("stock_in >= 0",name="ck_inventory_stock_in_positive",),

        CheckConstraint("stock_out >= 0",name="ck_inventory_stock_out_positive",),

        CheckConstraint("available_stock >= 0",name="ck_inventory_available_stock_positive",),

        CheckConstraint("reorder_level >= 0",name="ck_inventory_reorder_level_positive",),)

    # ======================================================
    # HELPER PROPERTIES
    # ======================================================

    @property
    def is_out_of_stock(self) -> bool:
        """
        Product completely unavailable.
        """
        return self.available_stock <= 0

    @property
    def is_low_stock(self) -> bool:
        """
        Reached reorder threshold.
        """
        return (
            self.available_stock
            <= self.reorder_level
        )

    @property
    def stock_percentage(self) -> float:
        """
        Inventory utilization percentage.
        """

        if self.stock_in == 0:
            return 0

        return round(
            (self.available_stock / self.stock_in) * 100,
            2,
        )

    # ======================================================
    # INVENTORY OPERATIONS
    # ======================================================

    def add_stock(
        self,
        quantity: int,
    ) -> None:

        if quantity < 0:
            raise ValueError(
                "Quantity must be positive"
            )

        self.stock_in += quantity
        self.available_stock += quantity

    def remove_stock(
        self,
        quantity: int,
    ) -> None:

        if quantity < 0:
            raise ValueError(
                "Quantity must be positive"
            )

        if quantity > self.available_stock:
            raise ValueError(
                "Insufficient stock"
            )

        self.stock_out += quantity
        self.available_stock -= quantity

    # ======================================================
    # REPR
    # ======================================================

    def __repr__(self):

        return (
            f"<Inventory("
            f"id={self.id}, "
            f"product_id={self.product_id}, "
            f"available_stock={self.available_stock}"
            f")>"
        )