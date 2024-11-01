# flake8: noqa
from infrastructure.db.models.base import (Base, CreatedAtOnlyMixin,
                                           UpdatedAtOnlyMixin)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class RatingModel(Base, CreatedAtOnlyMixin, UpdatedAtOnlyMixin):
    __tablename__ = 'rating'

    id: Mapped[str] = mapped_column(primary_key=True)   # noqa A003
    workout_id: Mapped[str] = mapped_column(ForeignKey('workouts.id'), nullable=False)

    likes: Mapped[int] = mapped_column(default=0, nullable=False)
    dislikes: Mapped[int] = mapped_column(default=0, nullable=False)

    workout: Mapped['WorkoutModel'] = relationship(
        back_populates='rating',
    )
