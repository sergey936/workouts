from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class CommandHandlerNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self):
        return f"Handlers for command: {self.command_type} not found"
