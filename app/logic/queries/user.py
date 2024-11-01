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
    bot_api_token: str | None = None
    tg_user_id: str | None = None


@dataclass
class GetCurrentUserQueryHandler(BaseQueryHandler[GetCurrentUserQuery, User]):
    user_repository: BaseUserRepository
    config: Config

    async def handle(self, query: GetCurrentUserQuery) -> User:
        if query.tg_user_id and query.bot_api_token:
            if query.bot_api_token == self.config.bot_api_key:
                user = await self.user_repository.get_user_by_telegram_id(user_tg_id=query.tg_user_id)

                if user:
                    return user

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
