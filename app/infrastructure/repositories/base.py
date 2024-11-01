from abc import ABC
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker


@dataclass
class SQLAlchemyRepository(ABC):
    _sa_engine: AsyncEngine

    @property
    def _session(self) -> async_sessionmaker:
        return async_sessionmaker(bind=self._sa_engine, autoflush=False, expire_on_commit=False)
