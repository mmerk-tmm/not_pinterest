from typing import List
from pydantic import BaseModel
from backend.helpers.forms import form_body
from backend.core.config import env_config
from fastapi import Query

from backend.schemas.user import UserInfo


class CreateIdea(BaseModel):
    name: str = Query(..., max_length=env_config.get("VITE_MAX_IDEA_NAME_LENGTH"),
                      min_length=env_config.get("VITE_MIN_IDEA_NAME_LENGTH"))
    description: str = Query(..., max_length=env_config.get(
        "VITE_MAX_IDEA_DESCRIPTION_LENGTH"))


@form_body
class CreateIdeaForm(CreateIdea):
    ...


class Idea(CreateIdea):
    id: int
    created: str
    likes: int


class IdeaWithUser(Idea):
    user: UserInfo


class IdeaWithLike(Idea):
    liked: bool


class IdeaWithUserAndLike(IdeaWithUser, IdeaWithLike):
    ...


class IdeaKeyword(BaseModel):
    id: int
    name: str
    uses: int
