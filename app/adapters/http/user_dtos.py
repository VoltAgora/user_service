# app/adapters/http/user_dtos.py
import re
from pydantic import BaseModel, EmailStr, field_validator
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

    @field_validator("phone")
    @classmethod
    def phone_format(cls, v: Optional[str]) -> Optional[str]:
        """HU-08 CA4: Teléfono debe ser 10 dígitos (Colombia) o vacío."""
        if v is None or (isinstance(v, str) and v.strip() == ""):
            return None
        digits = re.sub(r"\D", "", v)
        if len(digits) != 10:
            raise ValueError("El teléfono debe tener 10 dígitos")
        return v.strip() or None

class ChangeRoleRequest(BaseModel):
    role: int  # 0 admin, 1 user, 2 moderator...