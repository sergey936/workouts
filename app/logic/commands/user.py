from dataclasses import dataclass

from domain.entities.trainer import Trainer
from domain.entities.user import User
from domain.service.password import PasswordService
from infrastructure.repositories.user.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.integration import (EmptyUserTGIdException,
                                          InvalidApiTokenException)
from logic.exceptions.user import (UserAlreadyExistsException,
                                   UserAlreadyHaveTelegramIDException,
                                   UserNotFoundByEmailException,
                                   UserWithThatTGIdAlreadyExistsException)
from settings.config import Config


@dataclass(frozen=True)
class CreateNewUserCommand(BaseCommand):
    name: str
    surname: str
    patronymic: str
    email: str
    password: str


@dataclass
class CreateNewUserCommandHandler(BaseCommandHandler[CreateNewUserCommand, None]):
    user_repository: BaseUserRepository
    password_service: PasswordService

    async def handle(self, command: CreateNewUserCommand) -> None:
        user = await self.user_repository.get_user_by_email(email=command.email)

        if user:
            raise UserAlreadyExistsException()

        hash_password = self.password_service.hash_password(command.password)

        user = User.create_user(
            name=command.name,
            surname=command.surname,
            patronymic=command.patronymic,
            email=command.email,
            password=hash_password,
        )

        await self.user_repository.add_user(user=user)


@dataclass(frozen=True)
class DeleteUserCommand(BaseCommand):
    email: str


@dataclass
class DeleteUserCommandHandler(BaseCommandHandler[DeleteUserCommand, None]):
    user_repository: BaseUserRepository

    async def handle(self, command: DeleteUserCommand) -> None:
        user = await self.user_repository.get_user_by_email(email=command.email)

        if not user:
            raise UserNotFoundByEmailException()

        return await self.user_repository.delete_user_by_id(user_id=user.oid)


@dataclass(frozen=True)
class UpdateUserCommand(BaseCommand):
    email: str
    name: str | None
    surname: str | None
    patronymic: str | None


@dataclass
class UpdateUserCommandHandler(BaseCommandHandler[UpdateUserCommand, None]):
    user_repository: BaseUserRepository

    async def handle(self, command: UpdateUserCommand) -> None:
        user = await self.user_repository.get_user_by_email(email=command.email)

        if not user:
            raise UserNotFoundByEmailException()

        edited_user = user.edit_user(
            name=command.name,
            surname=command.surname,
            patronymic=command.patronymic,
        )

        return await self.user_repository.update_user(
            user_id=edited_user.oid,
            name=edited_user.name.as_generic_type(),
            surname=edited_user.surname.as_generic_type(),
            patronymic=edited_user.patronymic.as_generic_type(),
        )


@dataclass(frozen=True)
class CreateTrainerCommand(BaseCommand):
    email: str


@dataclass
class CreateTrainerCommandHandler(BaseCommandHandler[CreateTrainerCommand, User]):
    user_repository: BaseUserRepository

    async def handle(self, command: CreateTrainerCommand) -> User:
        user = await self.user_repository.get_user_by_email(email=command.email)

        if not user:
            raise UserNotFoundByEmailException()

        trainer = Trainer.become_trainer(user=user)

        await self.user_repository.set_trainer_role(user_id=trainer.oid)

        return trainer


@dataclass(frozen=True)
class SetUserTgIdCommand(BaseCommand):
    email: str
    tg_user_id: str | None
    bot_api_token: str | None


@dataclass
class SetUserTgIdCommandHandler(BaseCommandHandler[SetUserTgIdCommand, None]):
    user_repository: BaseUserRepository
    config: Config

    async def handle(self, command: SetUserTgIdCommand) -> None:
        if command.tg_user_id:
            if not command.bot_api_token or command.bot_api_token != self.config.bot_api_key:
                raise InvalidApiTokenException()

            user = await self.user_repository.get_user_by_email(email=command.email)

            if not user:
                raise UserNotFoundByEmailException()

            if await self.user_repository.get_user_by_telegram_id(user_tg_id=command.tg_user_id):
                raise UserWithThatTGIdAlreadyExistsException()

            if user.telegram_id:
                raise UserAlreadyHaveTelegramIDException()

            user.set_tg_id(tg_user_id=command.tg_user_id)

            await self.user_repository.set_user_telegram_id(
                tg_user_id=command.tg_user_id,
                email=command.email,
            )

            return user
        raise EmptyUserTGIdException()
