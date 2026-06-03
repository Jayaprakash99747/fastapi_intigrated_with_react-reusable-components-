# from enum import Enum

# # Pagination
# DEFAULT_PAGE_SIZE = 20
# MAX_PAGE_SIZE = 100

# # File Upload
# ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]
# MAX_IMAGE_SIZE_MB = 5
# MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024

# # OTP / Reset
# RESET_CODE_EXPIRE_MINUTES = 15
# RESET_CODE_LENGTH = 6

# # Order
# ORDER_NUMBER_PREFIX = "ORD"

# # Cache TTL (seconds)
# CACHE_TTL_SHORT = 60        # 1 min
# CACHE_TTL_MEDIUM = 300      # 5 min
# CACHE_TTL_LONG = 3600       # 1 hour
# CACHE_TTL_DAY = 86400       # 24 hours

# # Payment
# PAYMENT_CURRENCY = "INR"
# RAZORPAY_CURRENCY = "INR"

# # Messages
# MSG_USER_NOT_FOUND = "User not found"
# MSG_PRODUCT_NOT_FOUND = "Product not found"
# MSG_ORDER_NOT_FOUND = "Order not found"
# MSG_CATEGORY_NOT_FOUND = "Category not found"
# MSG_INVALID_CREDENTIALS = "Invalid email or password"
# MSG_EMAIL_EXISTS = "Email already registered"
# MSG_USERNAME_EXISTS = "Username already taken"
# MSG_INACTIVE_ACCOUNT = "Account is deactivated"
# MSG_UNAUTHORIZED = "Not authorized to perform this action"
# MSG_INVALID_TOKEN = "Invalid or expired token"
# MSG_OUT_OF_STOCK = "Product is out of stock"
# MSG_COUPON_INVALID = "Invalid or expired coupon"
# MSG_COUPON_EXHAUSTED = "Coupon usage limit reached"
# MSG_PAYMENT_FAILED = "Payment failed"
# MSG_PAYMENT_SUCCESS = "Payment successful"





from enum import Enum


# ==========================================================
# USER ROLES
# ==========================================================

class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


# ==========================================================
# ORDER STATUS
# ==========================================================

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"
    REFUNDED = "refunded"


# ==========================================================
# PAYMENT STATUS
# ==========================================================

class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


# ==========================================================
# PAYMENT PROVIDERS
# ==========================================================

class PaymentProvider(str, Enum):
    RAZORPAY = "razorpay"
    STRIPE = "stripe"
    COD = "cod"


# ==========================================================
# TOKEN TYPES
# ==========================================================

class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    PASSWORD_RESET = "password_reset"
    EMAIL_VERIFICATION = "email_verification"


# ==========================================================
# CACHE KEYS
# ==========================================================

CACHE_USER = "user:{}"

CACHE_PRODUCT = "product:{}"

CACHE_CATEGORY = "category:{}"

CACHE_ORDER = "order:{}"

CACHE_CART = "cart:{}"

CACHE_WISHLIST = "wishlist:{}"

CACHE_COUPON = "coupon:{}"

CACHE_BANNER = "banner:{}"


# ==========================================================
# REDIS KEYS
# ==========================================================

REDIS_BLACKLIST_TOKEN = "blacklist:{}"

REDIS_REFRESH_TOKEN = "refresh:{}"

REDIS_OTP = "otp:{}"

REDIS_EMAIL_VERIFY = "email_verify:{}"

REDIS_RATE_LIMIT = "rate_limit:{}"

REDIS_USER_SESSION = "session:{}"


# ==========================================================
# PAGINATION
# ==========================================================

DEFAULT_PAGE = 1

DEFAULT_PAGE_SIZE = 20

MAX_PAGE_SIZE = 100


# ==========================================================
# FILE UPLOADS
# ==========================================================

MAX_IMAGE_SIZE = 5 * 1024 * 1024

MAX_DOCUMENT_SIZE = 10 * 1024 * 1024

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

ALLOWED_DOCUMENT_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
}


# ==========================================================
# PRODUCT
# ==========================================================

MIN_PRODUCT_PRICE = 1

MAX_PRODUCT_PRICE = 10000000

MIN_RATING = 1

MAX_RATING = 5


# ==========================================================
# INVENTORY
# ==========================================================

DEFAULT_REORDER_LEVEL = 10

LOW_STOCK_THRESHOLD = 5


# ==========================================================
# PASSWORD POLICY
# ==========================================================

PASSWORD_MIN_LENGTH = 8

PASSWORD_MAX_LENGTH = 128


# ==========================================================
# OTP
# ==========================================================

OTP_LENGTH = 6

OTP_EXPIRE_MINUTES = 10

OTP_MAX_ATTEMPTS = 5


# ==========================================================
# REGEX
# ==========================================================

EMAIL_REGEX = (
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

PHONE_REGEX = (
    r"^[6-9]\d{9}$"
)

PASSWORD_REGEX = (
    r"^(?=.*[a-z])"
    r"(?=.*[A-Z])"
    r"(?=.*\d)"
    r"(?=.*[@$!%*?&])"
    r"[A-Za-z\d@$!%*?&]{8,}$"
)


# ==========================================================
# RATE LIMITS
# ==========================================================

LOGIN_RATE_LIMIT = "5/minute"

REGISTER_RATE_LIMIT = "3/minute"

FORGOT_PASSWORD_RATE_LIMIT = "3/minute"

OTP_VERIFY_RATE_LIMIT = "5/minute"

DEFAULT_RATE_LIMIT = "100/minute"

PAYMENT_RATE_LIMIT = "20/minute"


# ==========================================================
# ORDER EVENTS
# ==========================================================

ORDER_CREATED = "order_created"

ORDER_CONFIRMED = "order_confirmed"

ORDER_SHIPPED = "order_shipped"

ORDER_DELIVERED = "order_delivered"

ORDER_CANCELLED = "order_cancelled"


# ==========================================================
# PAYMENT EVENTS
# ==========================================================

PAYMENT_CREATED = "payment_created"

PAYMENT_SUCCESS = "payment_success"

PAYMENT_FAILED = "payment_failed"

PAYMENT_REFUNDED = "payment_refunded"


# ==========================================================
# AUDIT ACTIONS
# ==========================================================

AUDIT_CREATE = "create"

AUDIT_UPDATE = "update"

AUDIT_DELETE = "delete"

AUDIT_LOGIN = "login"

AUDIT_LOGOUT = "logout"


# ==========================================================
# ERROR MESSAGES
# ==========================================================

USER_NOT_FOUND = "User not found"

INVALID_CREDENTIALS = "Invalid email or password"

ACCOUNT_DISABLED = "Account is disabled"

EMAIL_ALREADY_EXISTS = "Email already exists"

USERNAME_ALREADY_EXISTS = "Username already exists"

INVALID_TOKEN = "Invalid token"

TOKEN_EXPIRED = "Token expired"

PRODUCT_NOT_FOUND = "Product not found"

CATEGORY_NOT_FOUND = "Category not found"

ORDER_NOT_FOUND = "Order not found"

PAYMENT_NOT_FOUND = "Payment not found"

COUPON_NOT_FOUND = "Coupon not found"

REVIEW_NOT_FOUND = "Review not found"

INSUFFICIENT_STOCK = "Insufficient stock"

INVALID_COUPON = "Invalid coupon"

COUPON_EXPIRED = "Coupon expired"

PAYMENT_FAILED_MESSAGE = "Payment failed"

UNAUTHORIZED = "Unauthorized"

FORBIDDEN = "Permission denied"


# ==========================================================
# HTTP HEADERS
# ==========================================================

REQUEST_ID_HEADER = "X-Request-ID"

CORRELATION_ID_HEADER = "X-Correlation-ID"


# ==========================================================
# MIME TYPES
# ==========================================================

IMAGE_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

DOCUMENT_MIME_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


# ==========================================================
# WEBSOCKET CHANNELS
# ==========================================================

WS_NOTIFICATIONS = "notifications"

WS_ORDERS = "orders"

WS_PAYMENTS = "payments"


# ==========================================================
# DEFAULTS
# ==========================================================

DEFAULT_CURRENCY = "INR"

DEFAULT_COUNTRY = "India"

DEFAULT_LANGUAGE = "en"


# ==========================================================
# API TAGS
# ==========================================================

AUTH_TAG = "Authentication"

USER_TAG = "Users"

CATEGORY_TAG = "Categories"

PRODUCT_TAG = "Products"

CART_TAG = "Cart"

WISHLIST_TAG = "Wishlist"

ORDER_TAG = "Orders"

PAYMENT_TAG = "Payments"

REVIEW_TAG = "Reviews"

COUPON_TAG = "Coupons"

BANNER_TAG = "Banners"

INVENTORY_TAG = "Inventory"