from dataclasses import dataclass

from domain.entities.user import User
from domain.events.trainer import NewTrainerCreatedEvent
from domain.exceptions.trainer import AlreadyTrainerException
from domain.values.role import Role


@dataclass
class Trainer(User):

    @classmethod
    def become_trainer(cls, user: User) -> 'Trainer':
        if user.role == Role.USER:
            user.role = Role.TRAINER
            user.register_event(NewTrainerCreatedEvent)
        else:
            raise AlreadyTrainerException()

        return cls(
            oid=user.oid,
            created_at=user.created_at,
            name=user.name,
            surname=user.surname,
            patronymic=user.patronymic,
            email=user.email,
            password=user.password,
            telegram_id=user.telegram_id,
            role=user.role,
            is_active=user.is_active,
        )
