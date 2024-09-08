from application.api.schemas import BaseQueryResponseSchema
from domain.entities.workout import Workout
from pydantic import BaseModel


class WorkoutDetailSchema(BaseModel):
    id: str # noqa A003

    trainer_id: str
    title: str
    description: str
    file_path: str | None

    is_active: bool

    @classmethod
    def from_entity(cls, workout: Workout) -> 'WorkoutDetailSchema':
        return cls(
            id=workout.oid,
            trainer_id=workout.trainer_oid,
            title=workout.title.as_generic_type(),
            description=workout.description.as_generic_type(),
            file_path=workout.file_path,
            is_active=workout.is_active
        )


class UploadWorkoutFileSchema(BaseModel):
    workout_id: str


class CreateWorkoutSchema(BaseModel):
    title: str
    description: str


class DeleteWorkoutSchema(BaseModel):
    workout_id: str


class DeleteWorkoutResponseSchema(BaseModel):
    response: str = 'Workout deleted.'


class EditWorkoutSchema(BaseModel):
    workout_id: str
    title: str | None
    description: str | None


class WorkoutFilters(BaseModel):
    limit: int = 10
    offset: int = 0


class GetNotesQueryResponseSchema(BaseQueryResponseSchema[list[WorkoutDetailSchema]]):
    ...
