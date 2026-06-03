

this is i have
project/
│
├── app/
│ │
│ ├── main.py
│ ├── api/
│ │ ├── routers/
│ │ │ ├── user.p
│ │ │ ├── auth.py
│ │ │
│ │ │
│ │ └── dependencies.py
│ │
│ ├── core/
│ │ ├── config.py
│ │ ├── security.py
│ │ ├── database.py
│ │ ├── settings.py
│ │ └── constants.py
│ │
│ ├── models/
│ │
│ │
│ │
│ ├── schemas/
│ │
│ │
│ │
│ ├── crud/
│ │
│ │
│ │
│ ├── services/
│ │ ├── auth_service.py
│ │ ├── email_service.py
│ │ └── payment_service.py
│ │
│ ├── db/
│ │ ├── session.py
│ │ ├── base.py
│ │ └── init_db.py
│ │
│ ├── utils/
│ │ ├── helpers.py
│ │ ├── validators.py
│ │ ├── logger.py
│ │ └── file_handler.py
│ │
│ ├── middleware/
│ │ ├── auth.py
│ │ ├── logging.py
│ │ └── cors.py
│ │
│ ├── exceptions/
│ │ ├── handlers.py
│ │ └── custom_exceptions.py
│ │
│ ├── templates/
│ │
│ ├── static/
│ │
│ ├── background_tasks/
│ │ ├── celery_tasks.py
│ │ └── scheduler.py
│ │
│ ├── websocket/
│ │ └── notification.py
│ │
│ ├── permissions/
│ │ └── roles.py
│ │
│ └── tests/
│ ├── test_auth.py
│ └── test_user.py
│
├── alembic/
│
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
What Each Folder Does

1. main.py
   for this project i have a basic models :

```python
from sqlalchemy import (
    Column, ForeignKey, Integer, String, Float,
    DateTime, Boolean, Text, Enum, Index
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import enum


class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentProvider(str, enum.Enum):
    RAZORPAY = "razorpay"
    STRIPE = "stripe"
    COD = "cod"


# ─────────────────────────────────────────────
# User
# ─────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    phone = Column(String(15), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    profile_image = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    is_email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reset_codes = relationship("PasswordResetCode", back_populates="user", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
    wishlist_items = relationship("WishlistItem", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(500), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="refresh_tokens")


class PasswordResetCode(Base):
    __tablename__ = "password_reset_codes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reset_code = Column(String(20), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reset_codes")


# ─────────────────────────────────────────────
# Category & Product
# ─────────────────────────────────────────────
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    brand = Column(String(100), nullable=True)
    price = Column(Float, nullable=False)
    discount_percent = Column(Float, default=0)
    gst_percent = Column(Float, default=18)
    rating = Column(Float, default=0)
    stock_quantity = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="product")
    wishlist_items = relationship("WishlistItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    reviews = relationship("Review", back_populates="product")
    inventory = relationship("Inventory", back_populates="product", uselist=False)


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False)

    product = relationship("Product", back_populates="images")


# ─────────────────────────────────────────────
# Cart & Wishlist
# ─────────────────────────────────────────────
class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

    __table_args__ = (
        Index("ix_cart_user_product", "user_id", "product_id", unique=True),
    )


class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="wishlist_items")
    product = relationship("Product", back_populates="wishlist_items")

    __table_args__ = (
        Index("ix_wishlist_user_product", "user_id", "product_id", unique=True),
    )


# ─────────────────────────────────────────────
# Orders
# ─────────────────────────────────────────────
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0)
    discount_amount = Column(Float, default=0)
    shipping_address = Column(Text, nullable=False)
    tracking_number = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False)


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0)
    tax_amount = Column(Float, default=0)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")


# ─────────────────────────────────────────────
# Payment
# ─────────────────────────────────────────────
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), unique=True, nullable=False)
    provider = Column(Enum(PaymentProvider), nullable=False)
    provider_order_id = Column(String(200), nullable=True)
    provider_payment_id = Column(String(200), nullable=True)
    provider_signature = Column(String(500), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    failure_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order = relationship("Order", back_populates="payment")


# ─────────────────────────────────────────────
# Reviews
# ─────────────────────────────────────────────
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    is_verified_purchase = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    __table_args__ = (
        Index("ix_review_product_user", "product_id", "user_id", unique=True),
    )


# ─────────────────────────────────────────────
# Inventory
# ─────────────────────────────────────────────
class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True, nullable=False)
    stock_in = Column(Integer, default=0)
    stock_out = Column(Integer, default=0)
    available_stock = Column(Integer, default=0)
    reorder_level = Column(Integer, default=10)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product = relationship("Product", back_populates="inventory")


# ─────────────────────────────────────────────
# Coupon
# ─────────────────────────────────────────────
class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    discount_percent = Column(Float, nullable=False)
    max_uses = Column(Integer, default=100)
    current_uses = Column(Integer, default=0)
    min_order_amount = Column(Float, default=0)
    is_active = Column(Boolean, default=True)
    expiry_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# ─────────────────────────────────────────────
# Banner
# ─────────────────────────────────────────────
class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=False)
    button_text = Column(String(100), nullable=True)
    button_link = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
```

for this models i want models curds,routers,schemas and all files intigrate with all files code and i want a end to end full functional production level working code i want and
also i want end to end apis from login to payment gatway each and evey end point api i want with async ,security and prodction level i want so give me code file by file and folder by folder each folder file what we user in there i want all code
i will ask you folder wise code can you give me?




With the structure you've shown and the models you've provided, I can generate a complete production-style FastAPI backend, folder by folder, including:

### Core

<pre class="overflow-visible! px-0!" data-start="169" data-end="269"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>app/core/</span><br/><span>├── config.py</span><br/><span>├── settings.py</span><br/><span>├── database.py</span><br/><span>├── security.py</span><br/><span>└── constants.py</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Database

<pre class="overflow-visible! px-0!" data-start="284" data-end="345"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>app/db/</span><br/><span>├── base.py</span><br/><span>├── session.py</span><br/><span>└── init_db.py</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Models

<pre class="overflow-visible! px-0!" data-start="358" data-end="511"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>app/models/</span><br/><span>├── user.py</span><br/><span>├── product.py</span><br/><span>├── order.py</span><br/><span>├── payment.py</span><br/><span>├── review.py</span><br/><span>├── inventory.py</span><br/><span>├── coupon.py</span><br/><span>├── banner.py</span><br/><span>└── __init__.py</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Schemas

<pre class="overflow-visible! px-0!" data-start="525" data-end="719"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>app/schemas/</span><br/><span>├── auth.py</span><br/><span>├── user.py</span><br/><span>├── category.py</span><br/><span>├── product.py</span><br/><span>├── cart.py</span><br/><span>├── wishlist.py</span><br/><span>├── order.py</span><br/><span>├── payment.py</span><br/><span>├── review.py</span><br/><span>├── inventory.py</span><br/><span>├── coupon.py</span><br/><span>└── banner.py</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### CRUD

<pre class="overflow-visible! px-0!" data-start="730" data-end="909"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>app/crud/</span><br/><span>├── user.py</span><br/><span>├── category.py</span><br/><span>├── product.py</span><br/><span>├── cart.py</span><br/><span>├── wishlist.py</span><br/><span>├── order.py</span><br/><span>├── payment.py</span><br/><span>├── review.py</span><br/><span>├── inventory.py</span><br/><span>├── coupon.py</span><br/><span>└── banner.py</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Services

<pre class="overflow-visible! px-0!" data-start="924" data-end="1077"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>app/services/</span><br/><span>├── auth_service.py</span><br/><span>├── email_service.py</span><br/><span>├── payment_service.py</span><br/><span>├── order_service.py</span><br/><span>├── product_service.py</span><br/><span>└── user_service.py</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Routers

<pre class="overflow-visible! px-0!" data-start="1091" data-end="1298"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>app/api/routers/</span><br/><span>├── auth.py</span><br/><span>├── users.py</span><br/><span>├── categories.py</span><br/><span>├── products.py</span><br/><span>├── cart.py</span><br/><span>├── wishlist.py</span><br/><span>├── orders.py</span><br/><span>├── payments.py</span><br/><span>├── reviews.py</span><br/><span>├── inventory.py</span><br/><span>├── coupons.py</span><br/><span>└── banners.py</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Middleware

<pre class="overflow-visible! px-0!" data-start="1315" data-end="1381"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>app/middleware/</span><br/><span>├── auth.py</span><br/><span>├── logging.py</span><br/><span>└── cors.py</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Exceptions

<pre class="overflow-visible! px-0!" data-start="1398" data-end="1466"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>app/exceptions/</span><br/><span>├── custom_exceptions.py</span><br/><span>└── handlers.py</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Permissions

<pre class="overflow-visible! px-0!" data-start="1484" data-end="1525"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>app/permissions/</span><br/><span>└── roles.py</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Utils

<pre class="overflow-visible! px-0!" data-start="1537" data-end="1626"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>app/utils/</span><br/><span>├── validators.py</span><br/><span>├── helpers.py</span><br/><span>├── logger.py</span><br/><span>└── file_handler.py</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Authentication Features

<pre class="overflow-visible! px-0!" data-start="1656" data-end="1942"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>POST   /auth/register</span><br/><span>POST   /auth/login</span><br/><span>POST   /auth/refresh-token</span><br/><span>POST   /auth/logout</span><br/><span>POST   /auth/forgot-password</span><br/><span>POST   /auth/verify-reset-code</span><br/><span>POST   /auth/reset-password</span><br/><br/><span>GET    /users/me</span><br/><span>PUT    /users/profile</span><br/><span>PUT    /users/change-password</span><br/><span>DELETE /users/delete-account</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Category APIs

<pre class="overflow-visible! px-0!" data-start="1962" data-end="2083"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>POST   /categories</span><br/><span>GET    /categories</span><br/><span>GET    /categories/{id}</span><br/><span>PUT    /categories/{id}</span><br/><span>DELETE /categories/{id}</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Product APIs

<pre class="overflow-visible! px-0!" data-start="2102" data-end="2295"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>POST   /products</span><br/><span>GET    /products</span><br/><span>GET    /products/{id}</span><br/><span>PUT    /products/{id}</span><br/><span>DELETE /products/{id}</span><br/><br/><span>GET    /products/search</span><br/><span>GET    /products/featured</span><br/><span>GET    /products/category/{id}</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Cart APIs

<pre class="overflow-visible! px-0!" data-start="2311" data-end="2407"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>POST   /cart/add</span><br/><span>GET    /cart</span><br/><span>PUT    /cart/{id}</span><br/><span>DELETE /cart/{id}</span><br/><span>DELETE /cart/clear</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Wishlist APIs

<pre class="overflow-visible! px-0!" data-start="2427" data-end="2498"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>POST   /wishlist/add</span><br/><span>GET    /wishlist</span><br/><span>DELETE /wishlist/{id}</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Order APIs

<pre class="overflow-visible! px-0!" data-start="2515" data-end="2637"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>POST   /orders/create</span><br/><span>GET    /orders</span><br/><span>GET    /orders/{id}</span><br/><span>PUT    /orders/cancel/{id}</span><br/><span>PUT    /orders/status/{id}</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Payment APIs

<pre class="overflow-visible! px-0!" data-start="2656" data-end="2768"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>POST   /payments/create-order</span><br/><span>POST   /payments/verify</span><br/><span>POST   /payments/webhook</span><br/><span>GET    /payments/{id}</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Review APIs

<pre class="overflow-visible! px-0!" data-start="2786" data-end="2884"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>POST   /reviews</span><br/><span>GET    /reviews/product/{id}</span><br/><span>PUT    /reviews/{id}</span><br/><span>DELETE /reviews/{id}</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Coupon APIs

<pre class="overflow-visible! px-0!" data-start="2902" data-end="3009"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>POST   /coupons</span><br/><span>GET    /coupons</span><br/><span>POST   /coupons/apply</span><br/><span>PUT    /coupons/{id}</span><br/><span>DELETE /coupons/{id}</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Banner APIs

<pre class="overflow-visible! px-0!" data-start="3027" data-end="3112"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>POST   /banners</span><br/><span>GET    /banners</span><br/><span>PUT    /banners/{id}</span><br/><span>DELETE /banners/{id}</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class="h-full min-h-0 min-w-0"></div></div></div></div></div></div></pre>

### Production Features

* Async SQLAlchemy 2.0
* Async FastAPI
* PostgreSQL
* JWT Access Token
* JWT Refresh Token
* Password Reset OTP
* Role Based Access Control
* Pagination
* Search
* Sorting
* Filtering
* Soft Delete
* Redis Cache
* Celery Tasks
* Email Service
* Razorpay Integration
* Stripe Integration
* WebSocket Notifications
* Alembic Migrations
* Docker
* Pytest
* Logging
* Exception Handling
* Request Validation
* Response Models
* Dependency Injection
* OpenAPI Documentation
* Environment Configuration

One important note: generating  **the entire codebase in a single response would be hundreds of files and tens of thousands of lines** , which won't fit in one message.

The best approach is:

1. Start with `app/core/`
2. Then `app/db/`
3. Then `app/models/`
4. Then `app/schemas/`
5. Then `app/crud/`
6. Then `app/services/`
7. Then `app/api/routers/`
8. Then `main.py`
9. Then Docker, Alembic, Tests
