from dataclasses import dataclass

from domain.entities.user import User
from domain.service.password import PasswordService
from infrastructure.repositories.user.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.auth import UserAlreadyExistsException


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
