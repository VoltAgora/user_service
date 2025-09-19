from fastapi import APIRouter, Body, Header, Depends, HTTPException, status
from app.adapters.persistence.user_repository import UserRepositorySQL
from app.domain.services.user_service import UserService
from app.adapters.http.user_dtos import UpdateProfileRequest, ChangeRoleRequest
from app.infrastructure.response import ResultHandler
import os
from jose import JWTError, jwt

router = APIRouter(
    prefix="/users",
    tags=["User Service"]
)

user_repo = UserRepositorySQL()
user_service = UserService(user_repo)

def get_current_user(authorization: str = Header(...)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    if not authorization.startswith("Bearer "):
        token = authorization
    else:
        token = authorization.split(" ", 1)[1]

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

@router.get("/{user_id}")
def get_user(user_id: int):
    return user_service.get_user(user_id)

@router.put("/{user_id}")
def update_profile(user_id: int, body: UpdateProfileRequest = Body(...), current_user: dict = Depends(get_current_user)):
    result = user_service.update_profile(user_id, body, current_user)
    return result

@router.patch("/{user_id}/role")
def change_role(user_id: int, body: ChangeRoleRequest = Body(...), current_user: dict = Depends(get_current_user)):
    result = user_service.change_role(user_id, body, current_user)
    return result