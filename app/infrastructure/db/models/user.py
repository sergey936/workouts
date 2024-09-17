# flake8: noqa
from domain.values.role import Role
from infrastructure.db.models.base import (Base, CreatedAtOnlyMixin,
                                           UpdatedAtOnlyMixin)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserModel(Base, CreatedAtOnlyMixin, UpdatedAtOnlyMixin):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(primary_key=True)   # noqa A003

    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str | None]

    password: Mapped[str | None]
    email: Mapped[str | None] = mapped_column(unique=True)

    telegram_id: Mapped[str | None] = mapped_column(unique=True)

    role: Mapped[Role] = mapped_column(default=Role.USER)
    is_active: Mapped[bool] = mapped_column(default=True)

    comments: Mapped[list['CommentModel']] = relationship(
        back_populates='user',
    )
