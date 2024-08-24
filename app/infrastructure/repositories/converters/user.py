from domain.entities.user import User as UserEntity
from infrastructure.db.models.user import User as UserModel


def convert_user_entity_to_db_model(user: UserEntity) -> UserModel:
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


def convert_user_db_model_to_entity(user: UserModel) -> UserEntity:
    user = UserEntity.create_user(
        name=user.name,
        surname=user.surname,
        patronymic=user.patronymic,
        email=user.email,
        password=user.password,
    )

    return user
