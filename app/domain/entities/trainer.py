from dataclasses import dataclass

from domain.entities.user import User
from domain.events.trainer import NewTrainerCreatedEvent
from domain.exceptions.trainer import AlreadyTrainerException
from domain.values.role import Role


@dataclass
class Trainer(User):

    def become_trainer(self):
        if self.role == Role.USER:
            self.role = Role.TRAINER
            self.register_event(NewTrainerCreatedEvent)
        else:
            raise AlreadyTrainerException()
