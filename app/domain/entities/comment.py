from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.events.feedback import NewCommentCreatedEvent, CommentDeletedEvent
from domain.values.workout import Text


@dataclass
class Comment(BaseEntity):
    workout_id: str
    user_id: str

    text_content: Text

    visible: bool = True

    def create_feedback(
            self,
            workout_id: str,
            user_id: str,
            text_content: Text
    ):
        self._events.append(NewCommentCreatedEvent)
        return Comment(
            workout_id=workout_id,
            user_id=user_id,
            text_content=text_content
        )

    def delete_feedback(
            self,
            feedback_id: str,
            user_id: str
    ):
        if self.oid == feedback_id and self.user_id == user_id:
            self._events.append(CommentDeletedEvent)
            self.visible = False
