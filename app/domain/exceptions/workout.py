from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass
class TooLongTitleException(ApplicationException):

    @property
    def message(self):
        return "Title too long. (Max length 100)"


@dataclass
class EmptyTitleException(ApplicationException):

    @property
    def message(self):
        return "Title cannot be empty."


@dataclass
class TooLongTextException(ApplicationException):

    @property
    def message(self):
        return "Text too long. (Max length 2000)"


@dataclass
class EmptyTextException(ApplicationException):

    @property
    def message(self):
        return "Text cannot be empty"


@dataclass
class NegativePriceException(ApplicationException):

    @property
    def message(self):
        return "Price can't be negative."
