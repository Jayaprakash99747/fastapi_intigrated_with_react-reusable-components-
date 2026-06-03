# ⚠️ IMPORTANT PRODUCTION NOTES
# ❗ This version includes a placeholder:
# token: str = Depends(lambda: None)
# You MUST replace it with:

# ✔ real JWT dependency
# ✔ decode_token middleware
# ✔ user_id extraction from token





from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.user_service import user_service
from app.services.auth_service import auth_service

from app.schemas.user import (
    UserUpdateSchema,
    PasswordChangeSchema,
    EmailUpdateSchema,
)

router = APIRouter(prefix="/users", tags=["Users"])


# =====================================================
# DEPENDENCY: GET CURRENT USER (JWT BASED)
# =====================================================

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(lambda: None),  # replace with real JWT dependency
):

    # NOTE: Replace this with real JWT decode dependency
    # Example:
    # payload = auth_service.decode_token(token)

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    return await user_service.get_user(db, user_id=1)


# =====================================================
# GET CURRENT USER PROFILE
# =====================================================

@router.get("/me")
async def get_me(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }


# =====================================================
# UPDATE PROFILE
# =====================================================

@router.put("/profile")
async def update_profile(
    payload: UserUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):

    updated_user = await user_service.update_profile(
        db,
        current_user,
        **payload.dict(exclude_unset=True),
    )

    return {
        "message": "Profile updated successfully",
        "user": updated_user,
    }


# =====================================================
# CHANGE PASSWORD
# =====================================================

@router.put("/change-password")
async def change_password(
    payload: PasswordChangeSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):

    success = await user_service.change_password(
        db,
        current_user,
        old_password=payload.old_password,
        new_password=payload.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Old password is incorrect",
        )

    return {"message": "Password changed successfully"}


# =====================================================
# UPDATE EMAIL
# =====================================================

@router.put("/change-email")
async def change_email(
    payload: EmailUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):

    updated_user = await user_service.update_email(
        db,
        current_user,
        new_email=payload.new_email,
    )

    return {
        "message": "Email updated successfully",
        "user": updated_user,
    }


# =====================================================
# DELETE ACCOUNT (SOFT DELETE)
# =====================================================

@router.delete("/delete-account")
async def delete_account(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):

    await user_service.delete_account(db, current_user)

    return {"message": "Account deactivated successfully"}


# =====================================================
# VERIFY EMAIL (OPTIONAL FLOW)
# =====================================================

@router.post("/verify-email")
async def verify_email(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):

    user = await user_service.verify_email(db, current_user)

    return {
        "message": "Email verified successfully",
        "user": user,
    }


# =====================================================
# ADMIN: LIST USERS
# =====================================================

@router.get("/admin/all")
async def list_users(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):

    users = await user_service.list_users(db, skip=skip, limit=limit)

    return {
        "total": len(users),
        "users": users,
    }


# =====================================================
# ADMIN: USER STATS
# =====================================================

@router.get("/admin/stats")
async def user_stats(
    db: AsyncSession = Depends(get_db),
):

    return await user_service.user_stats(db)