from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class NewCommentCreatedEvent(BaseEvent):
    event_title = "New comment created"

    comment_id: str
    user_id: str
    workout_id: str

    text_content: str


@dataclass
class CommentDeletedEvent(BaseEvent):
    event_title = "Comment deleted"

    comment_id: str
    user_id: str
    workout_id: str
