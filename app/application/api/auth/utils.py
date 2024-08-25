from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from logic.init import get_container
from logic.mediator.base import Mediator
from logic.queries.user import GetCurrentUserQuery
from punq import Container

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        container: Container = Depends(get_container),
) -> User:
    mediator: Mediator = container.resolve(Mediator)

    try:
        user = await mediator.handle_query(
            GetCurrentUserQuery(
                token=token,
            ),
        )
    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return user
