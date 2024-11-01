from dataclasses import dataclass

from domain.exceptions.workout import (EmptyTextException, EmptyTitleException,
                                       NegativePriceException,
                                       TooLongTextException,
                                       TooLongTitleException)
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Title(BaseValueObject):
    def validate(self):
        if not self.value:
            raise EmptyTitleException()

        if len(self.value) > 100:
            raise TooLongTitleException()

    def as_generic_type(self):
        if not self.value:
            return None

        return str(self.value)


@dataclass(frozen=True)
class Text(BaseValueObject):
    def validate(self):
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 2000:
            raise TooLongTextException()

    def as_generic_type(self):
        if not self.value:
            return None

        return str(self.value)


@dataclass(frozen=True)
class Price(BaseValueObject):
    def validate(self):

        if int(self.value) < 0:
            raise NegativePriceException()

    def as_generic_type(self):
        if not self.value:
            return None

        return int(self.value)
