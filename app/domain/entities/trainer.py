from dataclasses import dataclass

from domain.entities.user import User
from domain.events.trainer import NewTrainerCreatedEvent
from domain.exceptions.trainer import AlreadyTrainerException
from domain.values.role import Role
from domain.values.trainer import Like, DisLike, Rating


@dataclass
class Trainer(User):
    likes: Like = Like(0)
    dislikes: DisLike = DisLike(0)
    rating: Rating = Rating(0)

    def become_trainer(self):
        if self.role == Role.user:
            self.role = Role.trainer
            self._events.append(NewTrainerCreatedEvent)
        else:
            raise AlreadyTrainerException()

