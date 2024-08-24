from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    ...


class CreatedAtOnlyMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('UTC', now())"))


class UpdatedAtOnlyMixin:
    updated_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('UTC', now())"))
