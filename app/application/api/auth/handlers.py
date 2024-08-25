from application.api.auth.schemas import TokenSchema
from domain.exceptions.base import ApplicationException
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from logic.commands.auth import (AuthenticateUserCommand,
                                 CreateAccessTokenCommand)
from logic.init import get_container
from logic.mediator.base import Mediator
from punq import Container

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post(
    path="/token",
    status_code=status.HTTP_200_OK,
    description='Login with jwt token',
    response_model=TokenSchema,

)
async def login_for_access_token_handler(
    form_data: OAuth2PasswordRequestForm = Depends(),
    container: Container = Depends(get_container),
) -> TokenSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        user, *_ = await mediator.handle_command(
            AuthenticateUserCommand(
                email=form_data.username,
                password=form_data.password,
            ),
        )

        access_token, *_ = await mediator.handle_command(
            CreateAccessTokenCommand(
                data={
                    "email": user.email.as_generic_type(),
                    "telegram_id": user.telegram_id,
                },
            ),
        )

    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return TokenSchema(
        access_token=access_token,
        token_type="bearer",
    )
