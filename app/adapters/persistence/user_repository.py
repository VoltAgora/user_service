from app.domain.ports.db_port import UserRepositoryPort
from app.domain.models.user import User as DomainUser
from app.adapters.persistence.user_entity import User as UserEntity
from app.infrastructure.db import get_db
from sqlalchemy.orm import Session

class UserRepositorySQL(UserRepositoryPort):
    def __init__(self):
        pass

    def _get_db(self) -> Session:
        return next(get_db())

    def save(self, user: DomainUser) -> DomainUser:
        db = self._get_db()
        try:
            entity = UserEntity(
                document=user.document,
                name=user.name,
                lastname=user.lastname,
                phone=user.phone,
                email=user.email,
                created_at=user.created_at,
                is_active=user.is_active
            )
            db.add(entity)
            db.commit()
            db.refresh(entity)
            return DomainUser(
                id=entity.id,
                document=entity.document,
                name=entity.name,
                lastname=entity.lastname,
                phone=entity.phone,
                email=entity.email,
                created_at=entity.created_at,
                is_active=entity.is_active
            )
        finally:
            db.close()

    def get_by_id(self, user_id: int):
        db = self._get_db()
        try:
            e = db.query(UserEntity).filter(UserEntity.id == user_id).first()
            if not e:
                return None
            return DomainUser(
                id=e.id,
                document=e.document,
                name=e.name,
                lastname=e.lastname,
                phone=e.phone,
                email=e.email,
                created_at=e.created_at,
                is_active=e.is_active
            )
        finally:
            db.close()

    def get_by_document(self, document: str):
        db = self._get_db()
        try:
            e = db.query(UserEntity).filter(UserEntity.document == document).first()
            if not e:
                return None
            return DomainUser(
                id=e.id,
                document=e.document,
                name=e.name,
                lastname=e.lastname,
                phone=e.phone,
                email=e.email,
                created_at=e.created_at,
                is_active=e.is_active
            )
        finally:
            db.close()