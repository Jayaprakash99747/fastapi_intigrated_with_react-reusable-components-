from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    CheckConstraint,
)

from sqlalchemy.orm import relationship

from app.core.database import Base


# ==========================================================
# REVIEW
# ==========================================================

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer,primary_key=True,index=True,)

    product_id = Column(Integer,ForeignKey("products.id",ondelete="CASCADE",),nullable=False,index=True,)

    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE",),nullable=False,index=True,)

    rating = Column(Integer,nullable=False,)

    comment = Column(Text,nullable=True,)

    is_verified_purchase = Column(Boolean,default=False,nullable=False,)

    created_at = Column(DateTime,default=datetime.utcnow,nullable=False,)

    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False,)

    # ======================================================
    # RELATIONSHIPS
    # ======================================================

    product = relationship("Product",back_populates="reviews",lazy="joined",)

    user = relationship("User",back_populates="reviews",lazy="joined",)

    # ======================================================
    # CONSTRAINTS
    # ======================================================

    __table_args__ = (

        # One review per user per product
        Index("ix_review_product_user","product_id","user_id",unique=True,),

        # Rating between 1 and 5
        CheckConstraint("rating >= 1 AND rating <= 5",name="ck_review_rating",),)

    # ======================================================
    # HELPERS
    # ======================================================

    @property
    def rating_text(self) -> str:

        ratings = {
            1: "Poor",
            2: "Fair",
            3: "Good",
            4: "Very Good",
            5: "Excellent",
        }

        return ratings.get(
            self.rating,
            "Unknown",
        )

    # ======================================================
    # REPR
    # ======================================================

    def __repr__(self):

        return (
            f"<Review("
            f"id={self.id}, "
            f"product_id={self.product_id}, "
            f"user_id={self.user_id}, "
            f"rating={self.rating}"
            f")>"
        )