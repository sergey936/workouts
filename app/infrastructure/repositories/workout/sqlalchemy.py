from dataclasses import dataclass
from typing import Iterable

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
        db_workout = convert_workout_entity_to_db_model(workout=workout)
        async with self._session() as session:

            session.add(db_workout)
            await session.commit()

        return workout

    async def get_workout_by_id(self, workout_id: str) -> Workout | None:
        stmt = select(WorkoutModel).where(WorkoutModel.id == workout_id)
        async with self._session() as session:
            workout = await session.scalar(stmt)

        if workout:
            return convert_db_model_to_workout_entity(workout=workout)

    async def delete_workout_by_id(self, workout_id: str, trainer_id: str) -> None:
        stmt = delete(WorkoutModel).where(WorkoutModel.trainer_id == trainer_id, WorkoutModel.id == workout_id)
        async with self._session() as session:

            await session.execute(stmt)
            await session.commit()

    async def set_file_url(self, workout_id: str, trainer_id: str, file_url: str) -> None:
        stmt = (
            update(WorkoutModel)
            .where(WorkoutModel.trainer_id == trainer_id, WorkoutModel.id == workout_id)
            .values(file_url=file_url)
        )
        async with self._session() as session:
            await session.execute(stmt)
            await session.commit()

    async def edit_workout(self, workout_id: str, trainer_id: str, title: str, description: str) -> None:
        stmt = (
            update(WorkoutModel)
            .where(WorkoutModel.trainer_id == trainer_id, WorkoutModel.id == workout_id)
            .values(title=title, description=description)
        )
        async with self._session() as session:

            await session.execute(stmt)
            await session.commit()

    async def get_all_user_workouts(self, trainer_id: str, limit: int, offset: int) -> Iterable[Workout] | None:
        query = (
            select(WorkoutModel)
            .where(WorkoutModel.trainer_id == trainer_id)
            .limit(limit)
            .offset(offset)
        )
        async with self._session() as session:
            workouts = await session.scalars(query)

        return [convert_db_model_to_workout_entity(workout=workout) for workout in workouts]
