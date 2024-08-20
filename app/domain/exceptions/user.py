from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass
class EmptyValueException(ApplicationException):
    text: str

    @property
    def message(self):
        return f"{self.text} cannot be empty."


@dataclass
class TooLongValueException(ApplicationException):
    text: str

    @property
    def message(self):
        return f"{self.text} too long."


@dataclass
class EmptyEmailException(ApplicationException):

    @property
    def message(self):
        return "Email cannot be empty."


@dataclass
class InvalidEmailException(ApplicationException):

    @property
    def message(self):
        return "Invalid email."


@dataclass
class EmptyPasswordException(ApplicationException):

    @property
    def message(self):
        return "Password cannot be empty"


@dataclass
class UnhashedPasswordException(ApplicationException):

    @property
    def message(self):
        return "Password must be hashed"


@dataclass
class AccessDeniedException(ApplicationException):

    @property
    def message(self):
        return "You can't do this."


