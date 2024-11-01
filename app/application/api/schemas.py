from typing import Generic, TypeVar

from pydantic import BaseModel

IT = TypeVar("IT")


class BaseQueryResponseSchema(BaseModel, Generic[IT]):
    offset: int
    limit: int
    items: IT
