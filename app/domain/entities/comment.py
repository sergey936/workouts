from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.events.feedback import CommentDeletedEvent, NewCommentCreatedEvent
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
            text_content: Text,
    ):
        new_comment = Comment(
            workout_id=workout_id,
            user_id=user_id,
            text_content=text_content,
        )
        new_comment.register_event(NewCommentCreatedEvent)

        return new_comment

    def delete_feedback(
            self,
            feedback_id: str,
            user_id: str,
    ):
        if self.oid == feedback_id and self.user_id == user_id:
            self.register_event(CommentDeletedEvent)
            self.visible = False
