from application.api.auth.utils import get_current_user
from application.api.user.schemas import (UserCreateResponseSchema,
                                          UserCreateSchema, UserResponseSchema)
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from fastapi import APIRouter, Depends, HTTPException, status
from logic.commands.user import CreateNewUserCommand
from logic.mediator.base import Mediator
from punq import Container

router = APIRouter(
    prefix='/user',
    tags=['Users'],
)


@router.post(
    path='/register',
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
    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return UserCreateResponseSchema()


@router.get(
    path='/me',
    summary='Get current authenticated user',
    response_model=UserResponseSchema,
)
async def get_current_user(user: User = Depends(get_current_user)) -> UserResponseSchema:
    return UserResponseSchema.from_entity(user=user)
