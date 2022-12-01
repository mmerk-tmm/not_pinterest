from pydantic import BaseModel

from backend.schemas.user import UserInfo


class CreateIdea(BaseModel):
    name: str
    description: str


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
    # count: int
