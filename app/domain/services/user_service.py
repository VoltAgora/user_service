from app.domain.ports.db_port import UserRepositoryPort
from app.adapters.http.user_dtos import UserCreateRequest
from app.infrastructure.response import ResultHandler
from app.domain.models.user import User
from datetime import datetime
from zoneinfo import ZoneInfo
import os

bogota_tz = ZoneInfo("America/Bogota") if os.getenv("TZ", None) is None else ZoneInfo(os.getenv("TZ"))

class UserService:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def create_user(self, payload: UserCreateRequest):
        try:
            # check existing
            existing = self.user_repo.get_by_document(payload.document)
            if existing:
                return ResultHandler.bad_request(message="Documento ya existe")

            user = User(
                document=payload.document,
                name=payload.name,
                lastname=payload.lastname,
                phone=payload.phone,
                email=str(payload.email),
                created_at=datetime.now(bogota_tz),
                is_active=True
            )
            saved = self.user_repo.save(user)
            return ResultHandler.created(data={"id": saved.id, "email": saved.email}, message="Usuario creado")
        except Exception as e:
            print("Error create_user:", e)
            return ResultHandler.internal_error(message="Error interno")
    
    def get_user_by_id(self, user_id: int):
        try:
            u = self.user_repo.get_by_id(user_id)
            if not u:
                return ResultHandler.bad_request(message="Usuario no encontrado")
            return ResultHandler.success(data=u.__dict__)
        except Exception as e:
            print("Error get_user:", e)
            return ResultHandler.internal_error(message="Error interno")