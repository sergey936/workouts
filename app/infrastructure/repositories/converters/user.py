from domain.entities.user import User
from domain.values.user import Email, Name, Password, Patronymic, Surname
from infrastructure.db.models.user import UserModel


def convert_user_entity_to_db_model(user: User) -> UserModel:
    return UserModel(
        id=user.oid,
        name=user.name.as_generic_type(),
        surname=user.surname.as_generic_type(),
        patronymic=user.patronymic.as_generic_type(),
        password=user.password.as_generic_type(),
        email=user.email.as_generic_type(),
        telegram_id=user.telegram_id or None,
        role=user.role,
        is_active=user.is_active,
    )


def convert_user_db_model_to_entity(user: UserModel) -> User:
    user = User(
        oid=user.id,
        name=Name(user.name),
        surname=Surname(user.surname),
        patronymic=Patronymic(user.patronymic),
        email=Email(user.email),
        password=Password(user.password),
        telegram_id=user.telegram_id,
        role=user.role,
        is_active=user.is_active,
    )

    return user
