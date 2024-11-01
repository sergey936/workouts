from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass
class NegativeLikeException(ApplicationException):

    @property
    def message(self):
        return "Like count can't be negative."


@dataclass
class EmptyLikeException(ApplicationException):

    @property
    def message(self):
        return "Like count can't be empty."


@dataclass
class NegativeDislikeException(ApplicationException):

    @property
    def message(self):
        return "Dislike count can't be negative."


@dataclass
class EmptyDislikeException(ApplicationException):

    @property
    def message(self):
        return "Dislike count can't be empty."


@dataclass
class EmptyRatingException(ApplicationException):

    @property
    def message(self):
        return "Rating can't be empty."


@dataclass
class NegativeRatingException(ApplicationException):

    @property
    def message(self):
        return "Rating can't be Negative."


@dataclass
class AlreadyTrainerException(ApplicationException):

    @property
    def message(self):
        return "You already registered as TRAINER"
