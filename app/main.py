
from fastapi import FastAPI
from contextlib import asynccontextmanager

# ============================
# CORE IMPORTS
# ============================
from app.core.logging_configuration import settings
from app.db.init_db import init_db
# ============================
# MIDDLEWARE
# ============================
from app.middleware.logging import LoggingMiddleware
from app.middleware.cors import add_cors_middleware
from app.middleware.auth import AuthMiddleware

# ============================
# EXCEPTION HANDLERS
# ============================

from fastapi.staticfiles import StaticFiles


from app.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler,
)

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# ============================
# ROUTERS
# ============================
from app.api.routers import (
    auth,
    users,
    categories,
    products,
    cart,
    wishlist,
    orders,
    payments,
    reviews,
    inventory,
    coupons,
    banners,
    admin,
)
import os

# ============================
# APP LIFESPAN (PRODUCTION SAFE)
# ============================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup/shutdown events
    """

    # Startup
    print("🚀 Starting Application...")

    await init_db()  # auto-create tables (dev mode / bootstrap)

    print("✅ Database initialized")

    yield

    # Shutdown
    print(" Shutting down Application...")


# ============================
# FASTAPI APP INIT
# ============================

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Production Ready Ecommerce Backend (FastAPI + Async SQLAlchemy)",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

os.makedirs(
    "uploads/images",
    exist_ok=True
)
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

# ============================
# MIDDLEWARE REGISTRATION
# ============================

# app.add_middleware(LoggingMiddleware)
# app.add_middleware(AuthMiddleware)
add_cors_middleware(app)


# ============================
# EXCEPTION HANDLERS REGISTRATION
# ============================

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)


# ============================
# ROUTER REGISTRATION
# ============================

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(products.router, prefix="/api")
# app.include_router(cart.router, prefix="/api")
# app.include_router(wishlist.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
# app.include_router(payments.router, prefix="/api")
# app.include_router(reviews.router, prefix="/api")
# app.include_router(inventory.router, prefix="/api")
# app.include_router(coupons.router, prefix="/api")
app.include_router(banners.router, prefix="/api")
app.include_router(admin.router,prefix="/api")


# ============================
# HEALTH CHECK ENDPOINT
# ============================

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "Service is running",
        "version": settings.PROJECT_VERSION
    }


# ============================
# ROOT ENDPOINT
# ============================

@app.get("/")
async def root():
    return {
        "message": "Welcome to Production FastAPI Ecommerce Backend",
        "docs": "/docs"
    }



# orders list 
# order stats 
# products















# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.core.config import settings
# from app.db.session import engine
# from app.db.base import Base
# from app.api.routers import routers_apis
# # from app.middleware.logging import setup_loggings
# import asyncio
# from app.middleware.logging import LoggingMiddleware
# from app.exceptions.handlers import add_exception_handlers


# from app.middleware.auth import AuthMiddleware

# app = FastAPI()
# from fastapi import FastAPI
# from app.exceptions.handlers import (
#     http_exception_handler,
#     validation_exception_handler,
#     global_exception_handler,
# )
# from fastapi.exceptions import RequestValidationError
# from starlette.exceptions import HTTPException as StarletteHTTPException


# app.add_exception_handler(StarletteHTTPException, http_exception_handler)
# app.add_exception_handler(RequestValidationError, validation_exception_handler)
# app.add_exception_handler(Exception, global_exception_handler)
# from app.middleware.logging import LoggingMiddleware

# app.add_middleware(LoggingMiddleware)

# app.add_middleware(AuthMiddleware)


# app=FastAPI(
#     title="Constraction website",
#     description="modern website",
#     version="1.0.0",

# )
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.BACKEND_CORS_ORIGINS,
#     allow_credentials=True,
    
# )

# app.add_middleware(LoggingMiddleware)

# app.include_router(routers_apis.router,prefix=f"{settings.API_V1_STR}/auth",tags=['Auth'])

# # Routers
# # app.include_router(auth.router, prefix="/auth", tags=["auth"])
# # app.include_router(user.router, prefix="/users", tags=["users"])
# # Add more: products, cart, orders, payments, etc.

# @app.on_event("startup")
# async def startup_event():
#     async with engine.begin()as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     print("Application started successfully!")

# @app.get("/")
# async def root():
#     return {"message":'welcome to Constraction website APIs'}

# if __name__=="__main__":
#     import uvicorn
#     uvicorn.run("app.main:app",host="0.0.0.0",port=8000,reload=True)
