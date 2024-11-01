from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent


@dataclass
class NewUserCreatedEvent(BaseEvent):
    event_title: ClassVar[str] = 'New USER created'

    user_oid: str

    email: str
    name: str
    surname: str
    patronymic: str

    telegram_id: str | None


@dataclass
class UserChangeEmailEvent(BaseEvent):
    event_title: ClassVar[str] = 'User change email'

    user_oid: str
    email: str

    telegram_id: str | None


@dataclass
class UserChangePasswordEvent(BaseEvent):
    event_title: ClassVar[str] = 'User change password'

    user_oid: str
    email: str

    telegram_id: str | None


@dataclass
class UserDeletedEvent(BaseEvent):
    event_title: ClassVar[str] = 'User change email'

    user_oid: str
    is_active: bool

    telegram_id: str | None


@dataclass
class UserEditEvent(BaseEvent):
    event_title: ClassVar[str] = 'User edited'

    user_oid: str
