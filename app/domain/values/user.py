import re
from dataclasses import dataclass

from domain.exceptions.user import (EmptyEmailException,
                                    EmptyPasswordException,
                                    EmptyValueException, InvalidEmailException,
                                    InvalidTelegramIDTypeException,
                                    TooLongValueException,
                                    TooShortValueException,
                                    UnhashedPasswordException)
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Name(BaseValueObject):
    def validate(self):
        if not self.value:
            raise EmptyValueException(text='Name')

        if len(self.value) < 1:
            raise TooShortValueException(text="Name")

        if len(self.value) > 100:
            raise TooLongValueException(text="Name")

    def as_generic_type(self):
        if not self.value:
            return None

        return str(self.value)


@dataclass(frozen=True)
class Surname(BaseValueObject):
    def validate(self):
        if not self.value:
            raise EmptyValueException(text="Surname")

        if len(self.value) < 1:
            raise TooShortValueException(text="Surname")

        if len(self.value) > 100:
            raise TooLongValueException(text="Surname")

    def as_generic_type(self):
        if not self.value:
            return None

        return str(self.value)


@dataclass(frozen=True)
class Patronymic(BaseValueObject):
    def validate(self):
        if not self.value:
            raise EmptyValueException(text="Patronymic")

        if len(self.value) < 1:
            raise TooShortValueException(text="Patronymic")

        if len(self.value) > 100:
            raise TooLongValueException(text="Patronymic")

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class Email(BaseValueObject):
    def validate(self):
        if not self.value:
            raise EmptyEmailException()

        if not self._is_valid_email():
            raise InvalidEmailException()

    def _is_valid_email(self) -> bool:
        email_regex = re.compile(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        )
        return re.match(email_regex, str(self.value)) is not None

    def as_generic_type(self):
        if not self.value:
            return None

        return str(self.value)


@dataclass(frozen=True)
class Password(BaseValueObject):
    def validate(self):
        if not self.value:
            raise EmptyPasswordException()

        if not self.is_hashed():
            raise UnhashedPasswordException()

    def is_hashed(self) -> bool:
        pattern = re.compile(r'^[a-f0-9]{64}$', re.IGNORECASE)
        return bool(pattern.match(str(self.value)))

    def as_generic_type(self):
        if not self.value:
            return None

        return str(self.value)


@dataclass(frozen=True)
class TelegramID(BaseValueObject):
    def validate(self):

        if self.value and not str(self.value).isdigit:
            raise InvalidTelegramIDTypeException()

    def as_generic_type(self):
        if not self.value:
            return None

        return str(self.value)
