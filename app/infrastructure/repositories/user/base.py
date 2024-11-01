from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.user import User as UserEntity


@dataclass
class BaseUserRepository(ABC):

    @abstractmethod
    async def set_trainer_role(self, user_id: str) -> None:
        ...

    @abstractmethod
    async def add_user(self, user: UserEntity) -> None:
        ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserEntity | None:
        ...

    @abstractmethod
    async def delete_user_by_id(self, user_id: str) -> None:
        ...

    @abstractmethod
    async def update_user(
            self,
            user_id: str,
            name: str | None,
            surname: str | None,
            patronymic: str | None,
    ) -> None:
        ...

    @abstractmethod
    async def get_user_by_telegram_id(self, user_tg_id: str) -> UserEntity | None:
        ...

    @abstractmethod
    async def set_user_telegram_id(self, tg_user_id: str, email: str) -> None:
        ...
