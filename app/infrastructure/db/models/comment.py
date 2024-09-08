# flake8: noqa
from infrastructure.db.models.base import Base, CreatedAtOnlyMixin
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CommentModel(Base, CreatedAtOnlyMixin):
    __tablename__ = 'comments'

    id: Mapped[str] = mapped_column(String(), primary_key=True) # noqa A003

    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    workout_id: Mapped[str] = mapped_column(ForeignKey('workouts.id'))

    visible: Mapped[bool] = mapped_column(default=True, nullable=False)

    workout: Mapped['WorkoutModel'] = relationship(
        back_populates='comments',
    )

    user: Mapped['UserModel'] = relationship(
        back_populates='comments',
    )
