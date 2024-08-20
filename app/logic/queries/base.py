from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Any, Generic


@dataclass
class BaseQuery:
    ...


QT = TypeVar('QT', bound=BaseQuery)
QR = TypeVar('QR', bound=Any)


@dataclass
class BaseQueryHandler(ABC, Generic[QT, QR]):

    @abstractmethod
    async def handle(self, query: QT) -> QT:
        ...
