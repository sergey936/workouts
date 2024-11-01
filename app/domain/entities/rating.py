from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.values.trainer import DisLike, Like


@dataclass
class Rating(BaseEntity):
    workout_oid: str

    likes: Like
    dislike: DisLike

    def add_like(self):
        self.likes += 1

    def remove_lise(self):
        self.likes -= 1

    def add_dislike(self):
        self.dislike += 1

    def remove_dislike(self):
        self.dislike -= 1
