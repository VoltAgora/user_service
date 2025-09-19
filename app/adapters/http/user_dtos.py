# app/adapters/http/user_dtos.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserResponse(BaseModel):
    id: int
    document: str
    name: str
    lastname: str
    phone: Optional[str] = None
    email: EmailStr
    role: int
    is_active: bool

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class ChangeRoleRequest(BaseModel):
    role: int  # 0 admin, 1 user, 2 moderator...