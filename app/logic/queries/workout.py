from dataclasses import dataclass
from typing import Iterable

from domain.entities.workout import Workout
from infrastructure.repositories.user.base import BaseUserRepository
from infrastructure.repositories.workout.base import BaseWorkoutRepository
from logic.exceptions.user import UserNotFoundByEmailException
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass
class GetAllUserWorkoutsQuery(BaseQuery):
    limit: int
    offset: int
    email: str


@dataclass
class GetAllUserWorkoutsQueryHandler(BaseQueryHandler[GetAllUserWorkoutsQuery, Iterable[Workout]]):
    user_repository: BaseUserRepository
    workout_repository: BaseWorkoutRepository

    async def handle(self, query: GetAllUserWorkoutsQuery) -> Iterable[Workout]:
        user = await self.user_repository.get_user_by_email(email=query.email)

        if not user:
            raise UserNotFoundByEmailException()

        workouts = await self.workout_repository.get_all_user_workouts(
            trainer_id=user.oid,
            limit=query.limit,
            offset=query.offset,
        )

        return workouts



@dataclass
class GetAllWorkoutsQuery(BaseQuery):
    limit: int
    offset: int
    email: str
    desc: bool


@dataclass
class GetAllWorkoutsQueryHandler(BaseQueryHandler[GetAllWorkoutsQuery, Iterable[Workout]]):
    user_repository: BaseUserRepository
    workout_repository: BaseWorkoutRepository

    async def handle(self, query: GetAllWorkoutsQuery) -> Iterable[Workout]:
        user = await self.user_repository.get_user_by_email(email=query.email)

        if not user:
            raise UserNotFoundByEmailException()

        if not query.desc:
            workouts = await self.workout_repository.get_workouts_asc_order(
                limit=query.limit,
                offset=query.offset,
                desc=query.desc,
            )
        else:
            workouts = await self.workout_repository.get_workouts_desc_order(
                limit=query.limit,
                offset=query.offset,
                desc=query.desc,
            )

        return workouts
