from dataclasses import dataclass

from domain.exceptions.trainer import EmptyLikeException, NegativeLikeException, EmptyDislikeException, \
    NegativeDislikeException, EmptyRatingException, NegativeRatingException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Like(BaseValueObject):
    def validate(self):
        if not self.value():
            raise EmptyLikeException()

        if int(self.value) < 0:
            raise NegativeLikeException()

    def as_generic_type(self):
        return int(self.value)


@dataclass(frozen=True)
class DisLike(BaseValueObject):
    def validate(self):
        if not self.value():
            raise EmptyDislikeException()

        if int(self.value) < 0:
            raise NegativeDislikeException()

    def as_generic_type(self):
        return int(self.value)


@dataclass(frozen=True)
class Rating(BaseValueObject):
    def validate(self):
        if not self.value():
            raise EmptyRatingException()

        if int(self.value) < 0:
            raise NegativeRatingException()

    def as_generic_type(self):
        return int(self.value)
