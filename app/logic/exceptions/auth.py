from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class AuthException(LogicException):

    @property
    def message(self):
        return 'Auth exception.'


@dataclass
class UserAlreadyExistsException(AuthException):

    @property
    def message(self):
        return 'User already exists.'


@dataclass
class IncorrectCredentialsException(AuthException):

    @property
    def message(self):
        return 'Incorrect email or password.'


@dataclass
class CredentialsException(AuthException):

    @property
    def message(self):
        return 'Could not validate credentials.'
