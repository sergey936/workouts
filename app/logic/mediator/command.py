from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from logic.commands.base import BaseCommandHandler, CT, CR


@dataclass
class CommandMediator(ABC):
    commands_map: dict[CT: BaseCommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )

    @abstractmethod
    def register_command(self, command: CT, command_handlers: Iterable[BaseCommandHandler[CT, CR]]):
        ...

    @abstractmethod
    def handle_command(self, command: CT) -> Iterable[CR]:
        ...
