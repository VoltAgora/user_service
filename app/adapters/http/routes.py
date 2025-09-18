from fastapi import APIRouter, Body, Header
from app.domain.services.user_service import UserService
from app.adapters.persistence.user_repository import UserRepositorySQL
from app.infrastructure.response import ResultHandler
from app.adapters.http.user_dtos import UserCreateRequest, UserResponse

router = APIRouter(tags=["User Service"])

# DI
user_repo = UserRepositorySQL()
user_service = UserService(user_repo)

@router.get("/ping")
def ping():
    return ResultHandler.success(message="pong desde user service")

@router.post("/create")
def create_user(payload: UserCreateRequest = Body(...)):
    return user_service.create_user(payload)

@router.get("/{user_id}")
def get_user(user_id: int, authorization: str = Header(None)):
    return user_service.get_user_by_id(user_id)