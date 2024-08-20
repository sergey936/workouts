from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from logic.events.base import BaseEventHandler, ET, ER


@dataclass
class EventMediator(ABC):
    events_map: dict[ET: BaseEventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )

    @abstractmethod
    def register_event(self, event: ET, event_handlers: Iterable[BaseEventHandler[ET, ER]]):
        ...

    @abstractmethod
    def handle_event(self, events: Iterable[ET]) -> Iterable[ER]:
        ...
