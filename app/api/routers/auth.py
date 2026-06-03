from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.session import get_db
from app.services.auth_service import auth_service
from app.services.email_service import email_service
from app.schemas.auth import (
    RegisterSchema,
    LoginSchema,
    TokenSchema,
    RefreshTokenSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


# =====================================================
# REGISTER
# =====================================================

@router.post("/register", response_model=dict)
async def register(
    payload: RegisterSchema,
    db: AsyncSession = Depends(get_db),
):

    existing_user = await auth_service.get_user_by_email(db, payload.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user = await auth_service.register_user(
        db,
        username=payload.username,
        email=payload.email,
        password=payload.password,
    )

    # send welcome email (async fire-and-forget style)
    await email_service.send_welcome_email(
        to_email=user.email,
        username=user.username,
    )

    return {
        "message": "User registered successfully",
        "user_id": user.id,
    }


# =====================================================
# LOGIN
# =====================================================

@router.post("/login", response_model=TokenSchema)
async def login(
    payload: LoginSchema,
    db: AsyncSession = Depends(get_db),
):

    access_token, refresh_token, user = await auth_service.login_user(
        db,
        email=payload.email,
        password=payload.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


# =====================================================
# REFRESH TOKEN
# =====================================================

@router.post("/refresh-token")
async def refresh_token(
    payload: RefreshTokenSchema,
    db: AsyncSession = Depends(get_db),
):

    new_token = await auth_service.refresh_access_token(
        db,
        refresh_token=payload.refresh_token,
    )

    if not new_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    return {
        "access_token": new_token,
        "token_type": "bearer",
    }


# =====================================================
# LOGOUT
# =====================================================

@router.post("/logout")
async def logout(
    payload: RefreshTokenSchema,
    db: AsyncSession = Depends(get_db),
):

    success = await auth_service.logout_user(
        db,
        refresh_token=payload.refresh_token,
    )

    return {
        "message": "Logged out successfully" if success else "Invalid token",
    }


# =====================================================
# FORGOT PASSWORD
# =====================================================

@router.post("/forgot-password")
async def forgot_password(
    payload: ForgotPasswordSchema,
    db: AsyncSession = Depends(get_db),
):

    user = await auth_service.get_user_by_email(db, payload.email)

    if not user:
        return {"message": "If email exists, reset code sent"}

    reset_code = "123456"  # in real system → generate OTP

    await email_service.send_password_reset_email(
        to_email=user.email,
        reset_code=reset_code,
    )

    return {"message": "Reset code sent to email"}


# =====================================================
# RESET PASSWORD
# =====================================================

@router.post("/reset-password")
async def reset_password(
    payload: ResetPasswordSchema,
    db: AsyncSession = Depends(get_db),
):

    user = await auth_service.get_user_by_email(db, payload.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = auth_service.hash_password(payload.new_password)

    await db.commit()

    return {"message": "Password reset successful"}