from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt
from domain.entities.user import User
from domain.service.password import PasswordService
from infrastructure.repositories.user.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.auth import IncorrectCredentialsException
from settings.config import Config


@dataclass(frozen=True)
class AuthenticateUserCommand(BaseCommand):
    email: str
    password: str


@dataclass
class AuthenticateUserCommandHandler(BaseCommandHandler[AuthenticateUserCommand, User]):
    user_repository: BaseUserRepository
    password_service: PasswordService

    async def handle(self, command: AuthenticateUserCommand) -> User:
        user = await self.user_repository.get_user_by_email(email=command.email)

        if not user:
            raise IncorrectCredentialsException()

        if not self.password_service.check_password(
            plain_password=command.password,
            password=user.password,
        ):
            raise IncorrectCredentialsException()

        return user


@dataclass(frozen=True)
class CreateAccessTokenCommand(BaseCommand):
    data: dict


@dataclass
class CreateAccessTokenCommandHandler(BaseCommandHandler[CreateAccessTokenCommand, str]):
    config: Config

    async def handle(self, command: CreateAccessTokenCommand) -> str:
        expires_delta = timedelta(minutes=self.config.token_expire_min)
        to_encode = command.data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)

        return encoded_jwt
