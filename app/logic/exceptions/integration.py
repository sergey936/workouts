from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class IntegrationException(LogicException):

    @property
    def message(self):
        return 'Service integration exception.'


@dataclass
class InvalidApiTokenException(IntegrationException):

    @property
    def message(self):
        return 'Invalid api token.'


@dataclass
class EmptyUserTGIdException(IntegrationException):

    @property
    def message(self):
        return 'Request dont have user tg id.'
