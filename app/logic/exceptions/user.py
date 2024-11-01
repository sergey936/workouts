from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class NotFoundException(LogicException):

    @property
    def message(self):
        return 'Not found exception.'


@dataclass
class UserAlreadyExistsException(LogicException):

    @property
    def message(self):
        return 'User already exists.'


@dataclass
class UserNotFoundByEmailException(NotFoundException):

    @property
    def message(self):
        return 'User with that email not found.'


@dataclass
class NotTrainerException(LogicException):

    @property
    def message(self):
        return 'You not a trainer'


@dataclass
class UserNotFoundByTgIdException(NotFoundException):

    @property
    def message(self):
        return 'User with that tg id not found.'


@dataclass
class UserAlreadyHaveTelegramIDException(LogicException):

    @property
    def message(self):
        return 'This user already have tg id'


@dataclass
class UserWithThatTGIdAlreadyExistsException(LogicException):

    @property
    def message(self):
        return 'User with that tg id already exist.'
