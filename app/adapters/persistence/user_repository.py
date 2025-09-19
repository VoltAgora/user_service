from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.adapters.persistence.user_entity import User as UserEntity
from app.infrastructure.db import get_db
from sqlalchemy.exc import SQLAlchemyError

class UserRepositorySQL:
    def __init__(self):
        pass

    def _get_db_session(self) -> Session:
        gen = get_db()
        return next(gen)

    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        db = self._get_db_session()
        try:
            return db.query(UserEntity).filter(UserEntity.id == user_id).first()
        except SQLAlchemyError as e:
            raise
        finally:
            db.close()

    def get_by_email(self, email: str) -> Optional[UserEntity]:
        db = self._get_db_session()
        try:
            return db.query(UserEntity).filter(UserEntity.email == email).first()
        except SQLAlchemyError as e:
            raise
        finally:
            db.close()

    def get_by_document(self, document: str) -> Optional[UserEntity]:
        db = self._get_db_session()
        try:
            return db.query(UserEntity).filter(UserEntity.document == document).first()
        except SQLAlchemyError as e:
            raise
        finally:
            db.close()

    # Ahora acepta un dict con los campos a actualizar
    def update_profile(self, user_id: int, updates: Dict[str, Any]) -> Optional[UserEntity]:
        """
        updates: dict con keys opcionales: name, lastname, phone, email
        """
        db = self._get_db_session()
        try:
            user = db.query(UserEntity).filter(UserEntity.id == user_id).first()
            if not user:
                return None

            # Solo actualizar si viene en updates
            if "name" in updates and updates["name"] is not None:
                user.name = updates["name"]
            if "lastname" in updates and updates["lastname"] is not None:
                user.lastname = updates["lastname"]
            if "phone" in updates:
                user.phone = updates["phone"]
            if "email" in updates and updates["email"] is not None:
                user.email = updates["email"]

            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            db.rollback()
            print("Error repo.update_profile:", e)
            raise
        finally:
            db.close()

    def change_role(self, user_id: int, role: int) -> Optional[UserEntity]:
        db = self._get_db_session()
        try:
            user = db.query(UserEntity).filter(UserEntity.id == user_id).first()
            if not user:
                return None
            user.role = role
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except SQLAlchemyError as e:
            db.rollback()
            raise
        finally:
            db.close()