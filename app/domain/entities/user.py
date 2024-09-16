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
            telegram_id: str | None,
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
            telegram_id=telegram_id,
        )
        new_user.register_event(NewUserCreatedEvent)

        return new_user

    def change_password(self, password: Password) -> None:
        self.password = password
        self.register_event(UserChangePasswordEvent)

    def change_email(self, email: Email) -> None:
        self.email = email
        self.register_event(UserChangeEmailEvent)

    def delete_user(self) -> None:
        self.is_active = False
        self.register_event(UserDeletedEvent)

    def edit_user(
            self,
            name: str | None = None,
            surname: str | None = None,
            patronymic: str | None = None,
    ) -> 'User':

        self.name = Name(name) if name else self.name
        self.surname = Surname(surname) if surname else self.surname
        self.patronymic = Patronymic(patronymic) if patronymic else self.patronymic
        self.register_event(UserEditEvent)

        return self

    def set_tg_id(
            self,
            tg_user_id: str,
    ) -> None:
        self.telegram_id = tg_user_id
