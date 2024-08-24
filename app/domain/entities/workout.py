from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.entities.trainer import Trainer
from domain.events.workout import DeleteWorkoutEvent, NewWorkoutCreatedEvent
from domain.exceptions.user import AccessDeniedException
from domain.values.role import Role
from domain.values.workout import Price, Text, Title


@dataclass
class Workout(BaseEntity):
    trainer_oid: str

    title: Title
    description: Text

    is_active: bool = True
    price: Price | None = None

    def create_workout(
            self,
            trainer: Trainer,
            title: Title,
            description: Text,
            price: Price | None,
    ):
        if trainer.role == Role.TRAINER:
            new_workout = Workout(
                trainer_oid=trainer.oid,
                title=title,
                description=description,
                price=price,
            )
            new_workout.register_event(NewWorkoutCreatedEvent)

            return new_workout

        raise AccessDeniedException()

    def delete_workout(
            self,
            trainer: Trainer,
    ):
        if trainer.role == Role.TRAINER:
            if self.trainer_oid == trainer.oid:
                self.is_active = False
                self.register_event(DeleteWorkoutEvent)

        raise AccessDeniedException()

    def edit_workout(
            self,
            trainer: Trainer,
            title: Title | None = None,
            description: Text | None = None,
    ):
        if trainer.role == Role.TRAINER:
            if self.trainer_oid == trainer.oid:
                self.title = title if title else self.title
                self.description = description if description else self.description

        raise AccessDeniedException()
