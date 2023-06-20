from datetime import datetime
from typing import List
from pydantic import BaseModel
from backend.helpers.forms import form_body
from backend.core.config import env_config
from fastapi import Query
from backend.schemas.keywords import Keyword

from backend.schemas.user import UserInfo


class BaseIdea(BaseModel):
    name: str = Query(..., max_length=int(env_config.get("VITE_MAX_IDEA_NAME_LENGTH")),
                      min_length=int(env_config.get("VITE_MIN_IDEA_NAME_LENGTH")))
    description: str = Query(..., max_length=int(env_config.get(
        "VITE_MAX_IDEA_DESCRIPTION_LENGTH")))


class CreateIdea(BaseIdea):
    ...
    keywords_ids: List[int]
    new_keywords: List[str]


class Idea(BaseIdea):
    id: int
    created: datetime
    likes: int
    keywords: List[Keyword]

    class Config:
        orm_mode = True


class IdeaWithUser(Idea):
    user: UserInfo

    class Config:
        orm_mode = True


class IdeaWithLike(Idea):
    liked: bool = False


class IdeaWithUserAndLike(IdeaWithUser, IdeaWithLike):

    class Config:
        orm_mode = True


class IdeaKeyword(BaseModel):
    id: int
    name: str
    uses: int
