from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from logic.queries.base import QT, BaseQueryHandler, QR


@dataclass
class QueryMediator(ABC):
    queries_map: dict[QT: BaseQueryHandler] = field(
        default_factory=dict,
        kw_only=True
    )

    @abstractmethod
    def register_query(self, query: QT, query_handler: BaseQueryHandler[QT, QR]):
        ...

    @abstractmethod
    def handle_query(self, query: QT) -> QR:
        ...
