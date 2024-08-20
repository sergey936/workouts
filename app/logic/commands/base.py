from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Any, Generic

from logic.mediator.event import EventMediator


@dataclass(frozen=True)
class BaseCommand:
    ...


CT = TypeVar('CT', bound=BaseCommand)
CR = TypeVar('CR', bound=Any)


@dataclass
class BaseCommandHandler(ABC, Generic[CT, CR]):
    _mediator: EventMediator

    @abstractmethod
    async def handle(self, command: CT) -> CR:
        ...
