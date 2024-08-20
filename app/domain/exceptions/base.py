from dataclasses import dataclass


@dataclass
class ApplicationException(BaseException):

    @property
    def message(self):
        return "Application Exception"

