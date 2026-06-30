from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False,index=True,)

    product_id = Column(Integer,ForeignKey("products.id", ondelete="CASCADE"),nullable=False,)

    quantity = Column(Integer, default=1)

# ✅ FIX: required for User.cart_items
    user = relationship("User",back_populates="cart_items")

    # (optional but recommended)
    product = relationship("Product")

class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False,index=True,)

    product_id = Column(Integer,ForeignKey("products.id", ondelete="CASCADE"),nullable=False,)

    # ✅ FIX: required for User.wishlist_items
    user = relationship("User",back_populates="wishlist_items")

    product = relationship("Product")