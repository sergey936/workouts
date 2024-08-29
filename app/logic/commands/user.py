from dataclasses import dataclass

from domain.entities.user import User
from domain.service.password import PasswordService
from infrastructure.repositories.user.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.user import (UserAlreadyExistsException,
                                   UserNotFoundByEmailException)


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
