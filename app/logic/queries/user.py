from dataclasses import dataclass

import jwt
from domain.entities.user import User
from infrastructure.repositories.user.base import BaseUserRepository
from jwt import InvalidTokenError
from logic.exceptions.auth import CredentialsException
from logic.queries.base import BaseQuery, BaseQueryHandler
from settings.config import Config


@dataclass
class GetCurrentUserQuery(BaseQuery):
    token: str


@dataclass
class GetCurrentUserQueryHandler(BaseQueryHandler[GetCurrentUserQuery, User]):
    user_repository: BaseUserRepository
    config: Config

    async def handle(self, query: GetCurrentUserQuery) -> User:
        try:
            payload = jwt.decode(query.token, self.config.secret_key, algorithms=[self.config.algorithm])
            email: str = payload.get("email")

            if not email:
                raise CredentialsException()

        except InvalidTokenError:
            raise CredentialsException()

        user = await self.user_repository.get_user_by_email(email=email)

        if not user:
            raise CredentialsException()

        return user
