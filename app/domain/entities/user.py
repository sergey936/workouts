from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.events.user import NewUserCreatedEvent, UserChangeEmailEvent, UserDeletedEvent, \
    UserChangePasswordEvent, UserEditEvent
from domain.values.role import Role
from domain.values.user import Name, Surname, Patronymic, Email, Password


@dataclass
class User(BaseEntity):
    name: Name
    surname: Surname
    patronymic: Patronymic

    email: Email
    password: Password
    telegram_id: str | None = None

    role: Role = Role.user
    is_active: bool = True

    def create_user(
            self,
            name: Name,
            surname: Surname,
            patronymic: Patronymic,
            email: Email,
            telegram_id: str | None,
            password: Password,
    ) -> 'User':
        self._events.append(NewUserCreatedEvent)
        return User(
            name=name,
            surname=surname,
            patronymic=patronymic,
            email=email,
            password=password,
            telegram_id=telegram_id,
        )

    def change_password(self, password: Password) -> 'User':
        self.password = password
        self._events.append(UserChangePasswordEvent)

    def change_email(self, email: Email) -> 'User':
        self.email = email
        self._events.append(UserChangeEmailEvent)

    def delete_user(self) -> None:
        self.is_active = False
        self._events.append(UserDeletedEvent)

    def edit_user(
            self,
            name: Name | None = None,
            surname: Surname | None = None,
            patronymic: Patronymic | None = None
    ):
        self.name = name if name else self.name
        self.surname = surname if surname else self.surname
        self.patronymic = patronymic if patronymic else self.patronymic
        self._events.append(UserEditEvent)
