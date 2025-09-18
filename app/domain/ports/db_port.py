from abc import ABC, abstractmethod
from app.domain.models.user import User

class UserRepositoryPort(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_document(self, document: str) -> User | None:
        raise NotImplementedError