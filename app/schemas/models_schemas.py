from pydantic import BaseModel,EmailStr
from typing import Optional
from main_models import UserRole
from datetime import datetime

class UserRegister(BaseModel):
    username:str
    email:EmailStr
    password:str
    phone:Optional[str]=None

class UserLogin(BaseModel):
    email=EmailStr
    passeword:str

class UserUpdate(BaseModel):
    username:Optional[str]=None
    phone:Optional[str]=None
    address:Optional[str]=None
    city:Optional[str]=None
    state:Optional[str]=None
    pincode:Optional[str]=None

class ChaneEmailSchema(BaseModel):
    new_emial:str

class ChangePasswordSchema(BaseModel):
    old_password:str
    new_password:str
    confirm_password:str
    
class UserResponse(BaseModel):
    id:int
    username:str
    email:str
    role:str

    class Config:
        from_attributes=True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone: str | None = None

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True