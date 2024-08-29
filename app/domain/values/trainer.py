from dataclasses import dataclass

from domain.exceptions.trainer import (EmptyDislikeException,
                                       EmptyLikeException,
                                       NegativeDislikeException,
                                       NegativeLikeException)
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Like(BaseValueObject):
    def validate(self):
        if not self.value():
            raise EmptyLikeException()

        if int(self.value) < 0:
            raise NegativeLikeException()

    def as_generic_type(self):
        if not self.value:
            return None

        return int(self.value)


@dataclass(frozen=True)
class DisLike(BaseValueObject):
    def validate(self):
        if not self.value():
            raise EmptyDislikeException()

        if int(self.value) < 0:
            raise NegativeDislikeException()

    def as_generic_type(self):
        if not self.value:
            return None

        return int(self.value)
