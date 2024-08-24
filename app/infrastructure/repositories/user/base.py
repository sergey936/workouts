from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.user import User as UserEntity
from infrastructure.db.models import User as UserModel


@dataclass
class BaseUserRepository(ABC):

    @abstractmethod
    async def add_user(self, user: UserEntity) -> None:
        ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserModel:
        ...
