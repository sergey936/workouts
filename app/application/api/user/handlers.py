from application.api.user.schemas import (UserCreateResponseSchema,
                                          UserCreateSchema)
from domain.exceptions.base import ApplicationException
from fastapi import APIRouter, Depends, HTTPException, status
from logic.commands.user import CreateNewUserCommand
from logic.mediator.base import Mediator
from punq import Container

router = APIRouter(
    prefix='/user',
    tags=['users'],
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
