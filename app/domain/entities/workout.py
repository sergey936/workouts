from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.entities.trainer import Trainer
from domain.events.workout import NewWorkoutCreatedEvent, DeleteWorkoutEvent
from domain.exceptions.user import AccessDeniedException
from domain.values.role import Role
from domain.values.trainer import Like, Rating
from domain.values.workout import Title, Text, Price


@dataclass
class Workout(BaseEntity):
    trainer_oid: str

    title: Title
    description: Text
    likes: Like
    rating: Rating

    is_active: bool = True

    price: Price | None = None

    def create_workout(
            self,
            trainer: Trainer,
            title: Title,
            description: Text,
            likes: Like,
            rating: Rating,
            price: Price | None
    ):
        if trainer.role == Role.trainer:
            self._events.append(NewWorkoutCreatedEvent)
            return Workout(
                trainer_oid=trainer.oid,
                title=title,
                description=description,
                likes=likes,
                rating=rating,
                price=price
            )
        raise AccessDeniedException()

    def delete_workout(
            self,
            trainer: Trainer,
    ):
        if trainer.role == Role.trainer:
            if self.trainer_oid == trainer.oid:
                self.is_active = False
                self._events.append(DeleteWorkoutEvent)

        raise AccessDeniedException()

    def edit_workout(
            self,
            trainer: Trainer,
            title: Title | None = None,
            description: Text | None = None
    ):
        if trainer.role == Role.trainer:
            if self.trainer_oid == trainer.oid:
                self.title = title if title else self.title
                self.description = description if description else self.description

        raise AccessDeniedException()
