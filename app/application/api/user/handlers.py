from application.api.auth.utils import get_current_user
from application.api.user.schemas import (DeleteUserResponseSchema,
                                          UpdateUserRequestSchema,
                                          UserCreateResponseSchema,
                                          UserCreateSchema, UserResponseSchema,
                                          UserUpdatedResponseSchema)
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from fastapi import APIRouter, Depends, HTTPException, status
from logic.commands.user import (CreateNewUserCommand, CreateTrainerCommand,
                                 DeleteUserCommand, UpdateUserCommand)
from logic.exceptions.auth import AuthException
from logic.exceptions.user import NotFoundException
from logic.mediator.base import Mediator
from punq import Container

router = APIRouter()


@router.get(
    path='/',
    summary='Get current authenticated user',
    response_model=UserResponseSchema,
)
async def get_current_user_handler(user: User = Depends(get_current_user)) -> UserResponseSchema:
    return UserResponseSchema.from_entity(user=user)


@router.post(
    path='/',
    summary='Create new user',
    response_model=UserCreateResponseSchema,
)
async def create_user_handler(
        schema: UserCreateSchema,
        container: Container = Depends(),
) -> UserCreateResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(
            CreateNewUserCommand(
                name=schema.name,
                surname=schema.surname,
                patronymic=schema.patronymic,
                email=schema.email,
                password=schema.password,
            ),
        )
    except AuthException as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': auth_error.message})

    except NotFoundException as not_found_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': not_found_error.message})

    except ApplicationException as app_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': app_error.message})

    return UserCreateResponseSchema()


@router.delete(
    path='/',
    summary='Delete user',
    response_model=DeleteUserResponseSchema,
)
async def delete_user_handler(
        user: User = Depends(get_current_user),
        container: Container = Depends(),
) -> DeleteUserResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(
            DeleteUserCommand(
                email=user.email,
            )
        )

    except AuthException as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': auth_error.message})

    except NotFoundException as not_found_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': not_found_error.message})

    except ApplicationException as app_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': app_error.message})

    return DeleteUserResponseSchema()


@router.put(
    path='/set-telegram-id',
    summary='Set telegram id for user',
    response_model=UserUpdatedResponseSchema,
)
async def set_telegram_id_handler(
        user: User = Depends(get_current_user),
        container: Container = Depends(),
) -> UserUpdatedResponseSchema:
    raise HTTPException(status_code=400, detail="Not working yet")


@router.put(
    path='/',
    summary='Update (name, surname, patronymic) if exists.',
    response_model=UserUpdatedResponseSchema,
)
async def update_user_handler(
        schema: UpdateUserRequestSchema,
        user: User = Depends(get_current_user),
        container: Container = Depends(),
) -> UserUpdatedResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(
            UpdateUserCommand(
                email=user.email.as_generic_type(),
                name=schema.name,
                surname=schema.surname,
                patronymic=schema.patronymic,
            )
        )

    except AuthException as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': auth_error.message})

    except NotFoundException as not_found_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': not_found_error.message})

    except ApplicationException as app_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': app_error.message})

    return UserUpdatedResponseSchema()


@router.put(
    path='/set-trainer',
    summary='Become a trainer',
    response_model=UserUpdatedResponseSchema
)
async def set_trainer_status_handler(
        user: User = Depends(get_current_user),
        container: Container = Depends(),
) -> UserUpdatedResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(
            CreateTrainerCommand(
                email=user.email.as_generic_type()
            )
        )

    except AuthException as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': auth_error.message})

    except NotFoundException as not_found_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': not_found_error.message})

    except ApplicationException as app_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': app_error.message})

    return UserUpdatedResponseSchema()
