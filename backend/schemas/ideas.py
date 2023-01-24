from typing import List
from pydantic import BaseModel
from backend.helpers.forms import form_body

from backend.schemas.user import UserInfo


class CreateIdea(BaseModel):
    name: str
    description: str
    # keywords: List[str]


@form_body
class CreateIdeaForm(CreateIdea):
    ...


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
