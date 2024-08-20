from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class NewTrainerCreatedEvent(BaseEvent):
    event_title = "New trener created"

    user_id: str
    email: str

    telegram_id: str | None = None
