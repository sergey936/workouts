from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Any, Generic


@dataclass(frozen=True)
class BaseEvent:
    ...


ET = TypeVar('ET', bound=BaseEvent)
ER = TypeVar('ER', bound=Any)


@dataclass
class BaseEventHandler(ABC, Generic[ET, ER]):

    @abstractmethod
    async def handle(self, event: ET) -> ER:
        ...
