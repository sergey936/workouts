from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.workout import Workout


@dataclass
class BaseWorkoutRepository(ABC):
    @abstractmethod
    async def add_workout(self, user_id: str, workout: Workout) -> Workout:
        ...

    @abstractmethod
    async def get_workout_by_id(self, user_id: str, workout_id: str) -> Workout | None:
        ...

    @abstractmethod
    async def delete_workout_by_id(self, workout_id: str, trainer_id: str) -> None:
        ...

    @abstractmethod
    async def set_file_url(self, workout_id: str, trainer_id: str, file_url: str) -> None:
        ...

    @abstractmethod
    async def edit_workout(self, workout_id: str, trainer_id: str, title: str, description: str) -> None:
        ...
