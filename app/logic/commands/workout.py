from dataclasses import dataclass
from io import BytesIO

from domain.entities.workout import Workout
from domain.values.role import Role
from infrastructure.repositories.user.base import BaseUserRepository
from infrastructure.repositories.workout.base import BaseWorkoutRepository
from infrastructure.services.s3.workout import WorkoutS3Service
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.user import (NotTrainerException,
                                   UserNotFoundByEmailException)
from logic.exceptions.workout import (InvalidWorkoutFileFormatException,
                                      NotAllowedWorkoutException,
                                      WorkoutNotFoundException)
from settings.config import Config


@dataclass(frozen=True)
class CreateWorkoutCommand(BaseCommand):
    email: str
    title: str
    description: str


@dataclass
class CreateWorkoutCommandHandler(BaseCommandHandler[CreateWorkoutCommand, Workout]):
    user_repository: BaseUserRepository
    workout_repository: BaseWorkoutRepository

    async def handle(self, command: CreateWorkoutCommand) -> Workout:
        user = await self.user_repository.get_user_by_email(email=command.email)

        if not user:
            raise UserNotFoundByEmailException()

        if user.role != Role.TRAINER:
            raise NotTrainerException()

        workout = Workout.create_workout(
            trainer=user,
            title=command.title,
            description=command.description,
        )

        await self.workout_repository.add_workout(
            user_id=user.oid,
            workout=workout,
        )

        return workout


@dataclass(frozen=True)
class DeleteWorkoutCommand(BaseCommand):
    email: str
    workout_id: str


@dataclass
class DeleteWorkoutCommandHandler(BaseCommandHandler[DeleteWorkoutCommand, None]):
    user_repository: BaseUserRepository
    workout_repository: BaseWorkoutRepository

    async def handle(self, command: DeleteWorkoutCommand) -> None:
        user = await self.user_repository.get_user_by_email(email=command.email)

        if not user:
            raise UserNotFoundByEmailException()

        if user.role != Role.TRAINER:
            raise NotTrainerException()

        workout = await self.workout_repository.get_workout_by_id(
            workout_id=command.workout_id,
            user_id=user.oid,
        )

        if not workout:
            raise WorkoutNotFoundException()

        await self.workout_repository.delete_workout_by_id(
            workout_id=workout.oid,
            trainer_id=user.oid
        )


@dataclass(frozen=True)
class UploadWorkoutCommand(BaseCommand):
    email: str
    workout_id: str
    file: BytesIO
    file_name: str
    file_format: str


@dataclass
class UploadWorkoutCommandHandler(BaseCommandHandler[UploadWorkoutCommand, Workout]):
    user_repository: BaseUserRepository
    workout_repository: BaseWorkoutRepository
    s3_service: WorkoutS3Service
    config: Config

    async def handle(self, command: UploadWorkoutCommand) -> Workout:
        user = await self.user_repository.get_user_by_email(email=command.email)

        if command.file_format not in self.config.valid_file_formats:
            raise InvalidWorkoutFileFormatException()

        if not user:
            raise UserNotFoundByEmailException()

        if user.role != Role.TRAINER:
            raise NotTrainerException()

        workout = await self.workout_repository.get_workout_by_id(
            workout_id=command.workout_id,
        )

        if not workout:
            raise WorkoutNotFoundException()

        if not workout.trainer_oid == user.oid:
            raise NotAllowedWorkoutException()

        file_type: str = command.file_name.split('.')[1]
        s3_file_url = await self.s3_service.upload_file(file=command.file, file_name=f'{workout.oid}.{file_type}')

        workout.set_file_path(file_path=s3_file_url)

        await self.workout_repository.set_file_url(
            workout_id=workout.oid,
            trainer_id=user.oid,
            file_url=s3_file_url,
        )

        return workout


@dataclass(frozen=True)
class EditWorkoutCommand(BaseCommand):
    email: str
    workout_id: str
    title: str
    description: str


@dataclass
class EditWorkoutCommandHandler(BaseCommandHandler[EditWorkoutCommand, Workout]):
    user_repository: BaseUserRepository
    workout_repository: BaseWorkoutRepository

    async def handle(self, command: EditWorkoutCommand) -> Workout:
        user = await self.user_repository.get_user_by_email(email=command.email)

        if not user:
            raise UserNotFoundByEmailException()

        if user.role != Role.TRAINER:
            raise NotTrainerException()

        workout = await self.workout_repository.get_workout_by_id(
            workout_id=command.workout_id,
            user_id=user.oid,
        )

        if not workout:
            raise WorkoutNotFoundException()

        if not workout.trainer_oid == user.oid:
            raise NotAllowedWorkoutException()

        workout.edit_workout(
            trainer=user,
            title=command.title,
            description=command.description,
        )

        await self.workout_repository.edit_workout(
            trainer_id=user.oid,
            workout_id=workout.oid,
            title=command.title if command.title else workout.title.as_generic_type(),
            description=command.description if command.description else workout.description.as_generic_type(),
        )

        return workout
