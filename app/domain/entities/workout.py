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
    file_path: str | None = None

    is_active: bool = True
    price: Price | None = None

    @classmethod
    def create_workout(
            cls,
            trainer: Trainer,
            title: str,
            description: str,
            price: Price | None = None,
    ) -> 'Workout':
        if trainer.role == Role.TRAINER:

            new_workout = Workout(
                trainer_oid=trainer.oid,
                title=Title(title),
                description=Text(description),
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
            title: str | None = None,
            description: str | None = None,
    ):
        if trainer.role != Role.TRAINER:
            raise AccessDeniedException()

        if self.trainer_oid != trainer.oid:
            raise AccessDeniedException()

        self.title = Title(title) if title else self.title
        self.description = Text(description) if description else self.description

    def set_file_path(self, file_path: str):
        self.file_path = file_path
