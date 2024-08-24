from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.events.user import (NewUserCreatedEvent, UserChangeEmailEvent,
                                UserChangePasswordEvent, UserDeletedEvent,
                                UserEditEvent)
from domain.values.role import Role
from domain.values.user import Email, Name, Password, Patronymic, Surname


@dataclass
class User(BaseEntity):
    name: Name
    surname: Surname
    patronymic: Patronymic

    email: Email
    password: Password
    telegram_id: str | None = None

    role: Role = Role.USER
    is_active: bool = True

    @classmethod
    def create_user(
            cls,
            name: str,
            surname: str,
            patronymic: str,
            email: str,
            password: str,
    ) -> 'User':
        name = Name(name)
        surname = Surname(surname)
        patronymic = Patronymic(patronymic)
        email = Email(email)
        password = Password(password)

        new_user = User(
            name=name,
            surname=surname,
            patronymic=patronymic,
            email=email,
            password=password,
        )
        new_user.register_event(NewUserCreatedEvent)

        return new_user

    def change_password(self, password: Password) -> 'User':
        self.password = password
        self.register_event(UserChangePasswordEvent)

    def change_email(self, email: Email) -> 'User':
        self.email = email
        self.register_event(UserChangeEmailEvent)

    def delete_user(self) -> None:
        self.is_active = False
        self.register_event(UserDeletedEvent)

    def edit_user(
            self,
            name: Name | None = None,
            surname: Surname | None = None,
            patronymic: Patronymic | None = None,
    ):
        self.name = name if name else self.name
        self.surname = surname if surname else self.surname
        self.patronymic = patronymic if patronymic else self.patronymic
        self.register_event(UserEditEvent)
