from functools import lru_cache

from aiobotocore.session import get_session
from domain.service.password import PasswordService
from infrastructure.db.main import build_sa_engine
from infrastructure.repositories.user.base import BaseUserRepository
from infrastructure.repositories.user.sqlaclhemy import \
    SQLAlchemyUserRepository
from infrastructure.repositories.workout.base import BaseWorkoutRepository
from infrastructure.repositories.workout.sqlalchemy import \
    SQLAlchemyWorkoutRepository
from infrastructure.services.s3.workout import WorkoutS3Service
from logic.commands.auth import (AuthenticateUserCommand,
                                 AuthenticateUserCommandHandler,
                                 CreateAccessTokenCommand,
                                 CreateAccessTokenCommandHandler)
from logic.commands.user import (CreateNewUserCommand,
                                 CreateNewUserCommandHandler,
                                 CreateTrainerCommand,
                                 CreateTrainerCommandHandler,
                                 DeleteUserCommand, DeleteUserCommandHandler,
                                 SetUserTgIdCommand, SetUserTgIdCommandHandler,
                                 UpdateUserCommand, UpdateUserCommandHandler)
from logic.commands.workout import (CreateWorkoutCommand,
                                    CreateWorkoutCommandHandler,
                                    DeleteWorkoutCommand,
                                    DeleteWorkoutCommandHandler,
                                    EditWorkoutCommand,
                                    EditWorkoutCommandHandler,
                                    UploadWorkoutCommand,
                                    UploadWorkoutCommandHandler)
from logic.mediator.base import Mediator
from logic.queries.user import GetCurrentUserQuery, GetCurrentUserQueryHandler
from logic.queries.workout import (GetAllUserWorkoutsQuery,
                                   GetAllUserWorkoutsQueryHandler)
from punq import Container, Scope
from settings.config import Config
from sqlalchemy.ext.asyncio import AsyncEngine


@lru_cache(1)
def get_container() -> Container:
    return init_container()


def init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    container.register(PasswordService, instance=PasswordService(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    container.register(AsyncEngine, factory=build_sa_engine, config=config, scope=Scope.transient)

    def init_user_repository() -> BaseUserRepository:

        return SQLAlchemyUserRepository(
            _sa_engine=container.resolve(AsyncEngine),

        )

    def init_workout_repository() -> BaseWorkoutRepository:

        return SQLAlchemyWorkoutRepository(
            _sa_engine=container.resolve(AsyncEngine)
        )

    def init_s3_workout_service() -> WorkoutS3Service:
        return WorkoutS3Service(
            session=get_session(),
            access_key=config.s3_access_key_id,
            secret_key=config.s3_secret_key,
            endpoint_url=config.s3_endpoint_url,
            bucket_name=config.s3_workout_bucket_name,
            config=config,
        )

    container.register(BaseWorkoutRepository, factory=init_workout_repository, scope=Scope.transient)
    container.register(BaseUserRepository, factory=init_user_repository, scope=Scope.transient)
    container.register(WorkoutS3Service, factory=init_s3_workout_service, scope=Scope.singleton)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # create Command handlers
        # User
        create_new_user_command_handler = CreateNewUserCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
            password_service=container.resolve(PasswordService),
        )

        delete_user_command_handler = DeleteUserCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
        )
        update_user_command_handler = UpdateUserCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
        )
        create_trainer_command_handler = CreateTrainerCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository)
        )
        set_telegram_user_id_command_handler = SetUserTgIdCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
            config=config,
        )

        # Auth
        authenticate_user_command_handler = AuthenticateUserCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
            password_service=container.resolve(PasswordService),
        )

        create_access_token_command_handler = CreateAccessTokenCommandHandler(
            _mediator=mediator,
            config=config,
        )

        # Workout
        create_workout_command_handler = CreateWorkoutCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
            workout_repository=container.resolve(BaseWorkoutRepository),
        )
        delete_workout_command_handler = DeleteWorkoutCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
            workout_repository=container.resolve(BaseWorkoutRepository),
        )
        upload_workout_file_command_handler = UploadWorkoutCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
            workout_repository=container.resolve(BaseWorkoutRepository),
            s3_service=container.resolve(WorkoutS3Service),
            config=config,
        )
        edit_workout_command_handler = EditWorkoutCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
            workout_repository=container.resolve(BaseWorkoutRepository),
        )

        # create Query handlers
        # User
        get_current_user_query_handler = GetCurrentUserQueryHandler(
            user_repository=container.resolve(BaseUserRepository),
            config=config,
        )

        # Workouts
        get_all_user_workouts_query_handler = GetAllUserWorkoutsQueryHandler(
            user_repository=container.resolve(BaseUserRepository),
            workout_repository=container.resolve(BaseWorkoutRepository),
        )

        # register Commands
        # User
        mediator.register_command(
            CreateNewUserCommand,
            [create_new_user_command_handler],
        )
        mediator.register_command(
            DeleteUserCommand,
            [delete_user_command_handler],
        )
        mediator.register_command(
            UpdateUserCommand,
            [update_user_command_handler],
        )
        mediator.register_command(
            CreateTrainerCommand,
            [create_trainer_command_handler],
        )
        mediator.register_command(
            SetUserTgIdCommand,
            [set_telegram_user_id_command_handler],
        )

        # Auth
        mediator.register_command(
            AuthenticateUserCommand,
            [authenticate_user_command_handler],
        )

        mediator.register_command(
            CreateAccessTokenCommand,
            [create_access_token_command_handler],
        )
        mediator.register_command(
            DeleteWorkoutCommand,
            [delete_workout_command_handler],
        )

        # Workout
        mediator.register_command(
            CreateWorkoutCommand,
            [create_workout_command_handler],
        )
        mediator.register_command(
            UploadWorkoutCommand,
            [upload_workout_file_command_handler],
        )
        mediator.register_command(
            EditWorkoutCommand,
            [edit_workout_command_handler]
        )
        # register Queries
        # User
        mediator.register_query(
            GetCurrentUserQuery,
            get_current_user_query_handler,
        )
        mediator.register_query(
            GetAllUserWorkoutsQuery,
            get_all_user_workouts_query_handler,
        )

        return mediator

    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)

    return container
