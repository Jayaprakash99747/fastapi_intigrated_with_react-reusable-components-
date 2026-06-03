from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db
from app.services.auth_service import register_user, authenticate_user
from app.schemas.auth import Token
from app.core.security import create_access_token, create_refresh_token

router = APIRouter()

@router.post("/register")
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await register_user(db, user_in)

@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    
    access = create_access_token({"sub": user.username})
    refresh = create_refresh_token({"sub": user.username})
    return {"access_token": access, "refresh_token": refresh}