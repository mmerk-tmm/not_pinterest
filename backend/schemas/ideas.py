from typing import List
from pydantic import BaseModel

from backend.schemas.user import UserInfo


class CreateIdea(BaseModel):
    name: str
    description: str
    keywords: List[str]


class Idea(CreateIdea):
    id: int
    created: str
    likes: int
    user: UserInfo


class IdeaWithLike(Idea):
    liked: bool


class Topic(BaseModel):
    id: int
    name: str


class IdeaKeyword(BaseModel):
    id: int
    name: str
    uses: int
