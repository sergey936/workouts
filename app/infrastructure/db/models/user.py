# flake8: noqa
from domain.values.role import Role
from infrastructure.db.models.base import (Base, CreatedAtOnlyMixin,
                                           UpdatedAtOnlyMixin)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base, CreatedAtOnlyMixin, UpdatedAtOnlyMixin):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(primary_key=True)   # noqa A003

    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str]

    password: Mapped[str]
    email: Mapped[str]

    telegram_id: Mapped[int | None]

    role: Mapped[Role] = mapped_column(default=Role.USER)
    is_active: Mapped[bool] = mapped_column(default=True)

    comments: Mapped[list['Comment']] = relationship(
        back_populates='user',
    )
