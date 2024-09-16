from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass
class NotFoundException(ApplicationException):

    @property
    def message(self):
        return 'Not found exception.'


@dataclass
class UserAlreadyExistsException(ApplicationException):

    @property
    def message(self):
        return 'User already exists.'


@dataclass
class UserNotFoundByEmailException(NotFoundException):

    @property
    def message(self):
        return 'User with that email not found.'


@dataclass
class NotTrainerException(ApplicationException):

    @property
    def message(self):
        return 'You not a trainer'


@dataclass
class UserNotFoundByTgIdException(NotFoundException):

    @property
    def message(self):
        return 'User with that tg id not found.'
