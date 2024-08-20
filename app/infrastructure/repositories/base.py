from abc import ABC
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SQLAlchemyRepository(ABC):
    _session: AsyncSession
