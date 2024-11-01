# flake8: noqa
from infrastructure.db.models.base import (Base, CreatedAtOnlyMixin,
                                           UpdatedAtOnlyMixin)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class WorkoutModel(Base, CreatedAtOnlyMixin, UpdatedAtOnlyMixin):
    __tablename__ = 'workouts'

    id: Mapped[str] = mapped_column(primary_key=True)   # noqa A003
    trainer_id: Mapped[str] = mapped_column(ForeignKey('users.id'))

    title: Mapped[str]
    description: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    price: Mapped[int] = mapped_column(default=0, nullable=False)

    file_url: Mapped[str | None]

    rating: Mapped['RatingModel'] = relationship(
        back_populates='workout',
    )

    comments: Mapped[list['CommentModel']] = relationship(
        back_populates='workout',
    )
