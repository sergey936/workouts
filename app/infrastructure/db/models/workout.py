# flake8: noqa
from infrastructure.db.models.base import (Base, CreatedAtOnlyMixin,
                                           UpdatedAtOnlyMixin)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Workout(Base, CreatedAtOnlyMixin, UpdatedAtOnlyMixin):
    __tablename__ = 'workouts'

    id: Mapped[str] = mapped_column(primary_key=True)   # noqa A003

    title: Mapped[str]
    description: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    price: Mapped[int] = mapped_column(default=0, nullable=False)

    rating: Mapped['Rating'] = relationship(
        back_populates='workout',
    )

    comments: Mapped[list['Comment']] = relationship(
        back_populates='workout',
    )
