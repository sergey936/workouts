from dataclasses import dataclass

from domain.entities.user import User as UserEntity
from domain.values.role import Role
from infrastructure.db.models import UserModel
from infrastructure.repositories.base import SQLAlchemyRepository
from infrastructure.repositories.converters.user import (
    convert_user_db_model_to_entity, convert_user_entity_to_db_model)
from infrastructure.repositories.user.base import BaseUserRepository
from sqlalchemy import delete, select, update


@dataclass
class SQLAlchemyUserRepository(SQLAlchemyRepository, BaseUserRepository):

    async def add_user(self, user: UserEntity) -> None:
        db_user = convert_user_entity_to_db_model(user=user)
        async with self._session() as session:
            session.add(db_user)

            await session.commit()

    async def get_user_by_email(self, email: str) -> UserEntity | None:
        async with self._session() as session:
            query = select(UserModel).where(UserModel.email == email)
            user = await session.scalar(query)

            if user:
                return convert_user_db_model_to_entity(user=user)

    async def delete_user_by_id(self, user_id: str) -> None:
        stmt = delete(UserModel).where(UserModel.id == user_id)
        async with self._session() as session:
            await session.execute(stmt)
            await session.commit()

    async def update_user(
            self,
            user_id: str,
            name: str | None,
            surname: str | None,
            patronymic: str | None,
    ) -> None:
        stmt = update(UserModel).where(UserModel.id == user_id).values(
            name=name,
            surname=surname,
            patronymic=patronymic,
        )
        async with self._session() as session:
            await session.execute(stmt)
            await session.commit()

    async def set_trainer_role(self, user_id: str) -> None:
        stmt = update(UserModel).where(UserModel.id == user_id).values(
            role=Role.TRAINER,
        )
        async with self._session() as session:
            await session.execute(stmt)
            await session.commit()
