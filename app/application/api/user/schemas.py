from domain.entities.user import User
from domain.values.role import Role
from pydantic import BaseModel, EmailStr


class UserResponseSchema(BaseModel):
    oid: str

    name: str
    surname: str
    patronymic: str

    email: str
    telegram_id: str | None = None

    role: Role
    is_active: bool

    @classmethod
    def from_entity(cls, user: User) -> 'UserCreateResponseSchema':
        return cls(
            oid=user.oid,
            name=user.name.as_generic_type(),
            surname=user.surname.as_generic_type(),
            patronymic=user.patronymic.as_generic_type(),
            email=user.email.as_generic_type(),
            telegram_id=user.telegram_id,
            role=user.role,
            is_active=user.is_active,
        )


class UserCreateSchema(BaseModel):
    name: str
    surname: str
    patronymic: str

    email: EmailStr
    password: str


class UserCreateResponseSchema(BaseModel):
    response: str = 'User created.'
