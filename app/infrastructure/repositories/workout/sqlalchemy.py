from dataclasses import dataclass

from domain.entities.workout import Workout
from infrastructure.db.models import WorkoutModel
from infrastructure.repositories.base import SQLAlchemyRepository
from infrastructure.repositories.converters.workout import (
    convert_db_model_to_workout_entity, convert_workout_entity_to_db_model)
from infrastructure.repositories.workout.base import BaseWorkoutRepository
from sqlalchemy import delete, select, update


@dataclass
class SQLAlchemyWorkoutRepository(SQLAlchemyRepository, BaseWorkoutRepository):
    async def add_workout(self, user_id: str, workout: Workout) -> Workout:
        async with self._session() as session:
            db_workout = convert_workout_entity_to_db_model(workout=workout)

            session.add(db_workout)
            await session.commit()

            return workout

    async def get_workout_by_id(self, user_id: str, workout_id: str) -> Workout | None:
        async with self._session() as session:
            stmt = select(WorkoutModel).where(WorkoutModel.trainer_id == user_id, WorkoutModel.id == workout_id)
            workout = await session.scalar(stmt)

            if workout:
                return convert_db_model_to_workout_entity(workout=workout)

    async def delete_workout_by_id(self, workout_id: str, trainer_id: str) -> None:
        async with self._session() as session:
            stmt = delete(WorkoutModel).where(WorkoutModel.trainer_id == trainer_id, WorkoutModel.id == workout_id)

            await session.execute(stmt)
            await session.commit()

    async def set_file_url(self, workout_id: str, trainer_id: str, file_url: str) -> None:
        async with self._session() as session:
            stmt = (
                update(WorkoutModel)
                .where(WorkoutModel.trainer_id == trainer_id, WorkoutModel.id == workout_id)
                .values(file_url=file_url)
            )
            await session.execute(stmt)
            await session.commit()

    async def edit_workout(self, workout_id: str, trainer_id: str, title: str, description: str) -> None:
        async with self._session() as session:
            stmt = (
                update(WorkoutModel)
                .where(WorkoutModel.trainer_id == trainer_id, WorkoutModel.id == workout_id)
                .values(title=title, description=description)
            )

            await session.execute(stmt)
            await session.commit()
