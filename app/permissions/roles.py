from typing import Callable, List

from fastapi import Depends, HTTPException, status

from app.api.dependencies import get_current_user
from app.models.user import User


# =====================================================
# ROLE CONSTANTS (SOURCE OF TRUTH)
# =====================================================

class Roles:
    CUSTOMER = "customer"
    ADMIN = "admin"
    STAFF = "staff"
    VENDOR = "vendor"


# =====================================================
# CORE ROLE CHECKER
# =====================================================

def require_roles(allowed_roles: List[str]) -> Callable:

    async def role_checker(
        user: User = Depends(get_current_user),
    ) -> User:

        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        return user

    return role_checker


# =====================================================
# PREDEFINED PERMISSION DEPENDENCIES
# =====================================================

# 👤 Any logged-in user
require_user = require_roles([
    Roles.CUSTOMER,
    Roles.ADMIN,
    Roles.STAFF,
    Roles.VENDOR,
])

# 🛠 Admin only
require_admin = require_roles([Roles.ADMIN])

# 🏬 Staff + Admin (management access)
require_staff = require_roles([Roles.ADMIN, Roles.STAFF])

# 🛍 Vendor + Admin (product owners)
require_vendor = require_roles([Roles.ADMIN, Roles.VENDOR])


# =====================================================
# STRICT ADMIN CHECK (OPTIONAL DIRECT USE)
# =====================================================

async def admin_only(
    user: User = Depends(get_current_user),
) -> User:

    if user.role != Roles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return user




# ------------------------------
# 2. Easy API Protection
# Example usage in routers:
# from app.permissions.roles import require_admin

# @router.post("/products")
# async def create_product(user=Depends(require_admin)):
#     return {"msg": "Only admin can create products"}