from dataclasses import dataclass

from logic.exceptions.base import LogicException
from logic.exceptions.user import NotFoundException


@dataclass
class WorkoutNotFoundException(NotFoundException):

    @property
    def message(self):
        return 'Workout not found.'


@dataclass
class NotAllowedWorkoutException(LogicException):

    @property
    def message(self):
        return 'Not your workout.'
