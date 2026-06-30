# # All product-related models are defined in app/models/user.py
# # This file exists for modular imports
# from app.models.user import (
#     Category,
#     Product,
#     ProductImage,
#     CartItem,
#     WishlistItem,
#     Order,
#     OrderItem,
#     Payment,
#     Review,
#     Inventory,
#     Coupon,
#     Banner,
#     OrderStatus,
#     PaymentStatus,
#     PaymentProvider,
# )

# __all__ = [
#     "Category", "Product", "ProductImage",
#     "CartItem", "WishlistItem",
#     "Order", "OrderItem", "Payment",
#     "Review", "Inventory", "Coupon", "Banner",
#     "OrderStatus", "PaymentStatus", "PaymentProvider",
# ]












from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from app.core.database import Base


# ==========================================================
# CATEGORY
# ==========================================================

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer,primary_key=True,index=True,)

    name = Column(String(100),unique=True,nullable=False,index=True,)

    description = Column(Text,nullable=True,)

    image_url = Column(String(500),nullable=True,)

    is_deleted = Column(Boolean,default=False,nullable=False,)

    created_at = Column(DateTime,default=datetime.utcnow,nullable=False,)

    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False,)

    products = relationship("Product",back_populates="category",lazy="selectin",)

    def __repr__(self):
        return (
            f"<Category(id={self.id}, "
            f"name='{self.name}')>"
        )


# ==========================================================
# PRODUCT
# ==========================================================

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer,primary_key=True,index=True,)

    category_id = Column(Integer,ForeignKey("categories.id"),nullable=False,index=True,)

    name = Column(String(200),nullable=False,index=True,)

    description = Column(Text,nullable=True,)

    brand = Column(String(100),nullable=True,)

    sku = Column(String(100),unique=True,nullable=True,index=True,)

    price = Column(Float,nullable=False,)

    discount_percent = Column(Float,default=0,nullable=False,)

    gst_percent = Column(Float,default=18,nullable=False,)

    rating = Column(Float,default=0,nullable=False,)

    stock_quantity = Column(Integer,default=0,nullable=False,)

    is_available = Column(Boolean,default=True,nullable=False,)

    is_featured = Column(Boolean,default=False,nullable=False,)

    is_deleted = Column(Boolean,default=False,nullable=False,)

    created_at = Column(DateTime,default=datetime.utcnow,nullable=False,)

    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False,)

    # ======================================================
    # RELATIONSHIPS
    # ======================================================

    category = relationship("Category",back_populates="products",lazy="joined",)

    images = relationship("ProductImage",back_populates="product",cascade="all, delete-orphan",passive_deletes=True,)

    cart_items = relationship("CartItem",back_populates="product",)

    wishlist_items = relationship("WishlistItem",back_populates="product",)

    order_items = relationship("OrderItem",back_populates="product",)

    reviews = relationship("Review",back_populates="product",)

    inventory = relationship("Inventory",back_populates="product",uselist=False,)

    def __repr__(self):
        return (
            f"<Product("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"price={self.price}"
            f")>"
        )


# ==========================================================
# PRODUCT IMAGE
# ==========================================================

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer,primary_key=True,index=True,)

    product_id = Column(Integer,ForeignKey("products.id",ondelete="CASCADE",),nullable=False,index=True,)

    image_url = Column(String(500),nullable=False,)

    is_primary = Column(Boolean,default=False,nullable=False,)

    created_at = Column(DateTime,default=datetime.utcnow,nullable=False,)

    product = relationship("Product",back_populates="images",)

    def __repr__(self):
        return (
            f"<ProductImage("
            f"id={self.id}, "
            f"product_id={self.product_id}"
            f")>"
        )