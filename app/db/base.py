# from app.core.database import Base

# # Register all models
# from app.models import (
#     User, RefreshToken, PasswordResetCode,
#     Category, Product, ProductImage,
#     CartItem, WishlistItem,
#     Order, OrderItem,
#     Payment,
#     Review,
#     Inventory,
#     Coupon,
#     Banner
# )





# app/db/base.py

from app.core.database import Base

# ==========================================================
# USER
# ==========================================================

from app.models.user import (
    User,
    RefreshToken,
    PasswordResetCode,
)

# ==========================================================
# CATEGORY / PRODUCT
# ==========================================================

from app.models.product import (
    Category,
    Product,
    ProductImage,
    
)

# ==========================================================
# CART / WISHLIST
# ==========================================================

from app.models.cart import (
    CartItem,
    WishlistItem,
)

# ==========================================================
# ORDER
# ==========================================================

from app.models.order import (
    Order,
    OrderItem,
)

# ==========================================================
# PAYMENT
# ==========================================================

from app.models.payment import (
    Payment,
)

# ==========================================================
# REVIEW
# ==========================================================

from app.models.review import (
    Review,
)

# ==========================================================
# INVENTORY
# ==========================================================

from app.models.inventory import (
    Inventory,
)

# ==========================================================
# COUPON
# ==========================================================

from app.models.coupon import (
    Coupon,
)

# ==========================================================
# BANNER
# ==========================================================

from app.models.banner import (
    HeroSection,
)

# ==========================================================
# EXPORT
# ==========================================================

__all__ = [
    "Base",

    "User",
    "RefreshToken",
    "PasswordResetCode",

    "Category",
    "Product",
    "ProductImage",

    "CartItem",
    "WishlistItem",

    "Order",
    "OrderItem",

    "Payment",

    "Review",

    "Inventory",

    "Coupon",

    "Banner",
]