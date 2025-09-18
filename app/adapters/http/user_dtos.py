from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreateRequest(BaseModel):
    document: str
    name: str
    lastname: str
    phone: Optional[str] = None
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    document: str
    name: str
    lastname: str
    phone: Optional[str]
    email: EmailStr