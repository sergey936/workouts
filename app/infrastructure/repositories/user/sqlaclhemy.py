from dataclasses import dataclass

from domain.entities.user import User as UserEntity
from infrastructure.db.models import User as UserModel
from infrastructure.repositories.base import SQLAlchemyRepository
from infrastructure.repositories.converters.user import \
    convert_user_entity_to_db_model
from infrastructure.repositories.user.base import BaseUserRepository
from sqlalchemy import select


@dataclass
class SQLAlchemyUserRepository(SQLAlchemyRepository, BaseUserRepository):

    async def add_user(self, user: UserEntity) -> None:
        async with self._session() as session:
            db_user = convert_user_entity_to_db_model(user=user)
            session.add(db_user)

            await session.commit()

    async def get_user_by_email(self, email: str) -> UserModel:
        async with self._session() as session:
            query = select(UserModel).where(UserModel.email == email)
            user = await session.scalar(query)

            return user
