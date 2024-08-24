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


class UserCreateSchema(BaseModel):
    name: str
    surname: str
    patronymic: str

    email: EmailStr
    password: str


class UserCreateResponseSchema(BaseModel):
    response: str = 'User created.'
