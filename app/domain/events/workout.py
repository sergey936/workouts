from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class NewWorkoutCreatedEvent(BaseEvent):
    event_title = "New workout created"

    workout_id: str
    trainer_id: str
    title: str
    price: str


@dataclass
class DeleteWorkoutEvent(BaseEvent):
    event_title = "Workout deleted"

    workout_id: str
    trainer_id: str
