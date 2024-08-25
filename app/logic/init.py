from functools import lru_cache

from domain.service.password import PasswordService
from infrastructure.db.main import build_sa_engine
from infrastructure.repositories.user.base import BaseUserRepository
from infrastructure.repositories.user.sqlaclhemy import \
    SQLAlchemyUserRepository
from logic.commands.auth import (AuthenticateUserCommand,
                                 AuthenticateUserCommandHandler,
                                 CreateAccessTokenCommand,
                                 CreateAccessTokenCommandHandler)
from logic.commands.user import (CreateNewUserCommand,
                                 CreateNewUserCommandHandler)
from logic.mediator.base import Mediator
from logic.queries.user import GetCurrentUserQuery, GetCurrentUserQueryHandler
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
    config = container.resolve(Config)

    container.register(AsyncEngine, factory=build_sa_engine, config=config, scope=Scope.transient)

    def init_user_repository() -> BaseUserRepository:

        return SQLAlchemyUserRepository(
            _sa_engine=container.resolve(AsyncEngine),

        )

    container.register(BaseUserRepository, factory=init_user_repository, scope=Scope.transient)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # create Command handlers
        # User
        create_new_user_command_handler = CreateNewUserCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
            password_service=container.resolve(PasswordService),
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

        # create Query handlers
        # User
        get_current_user_query_handler = GetCurrentUserQueryHandler(
            user_repository=container.resolve(BaseUserRepository),
            config=config,
        )

        # register Commands
        # User
        mediator.register_command(
            CreateNewUserCommand,
            [create_new_user_command_handler],
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
        # register Queries
        # User
        mediator.register_query(
            GetCurrentUserQuery,
            get_current_user_query_handler,
        )

        return mediator

    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)

    return container
