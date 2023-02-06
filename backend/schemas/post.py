from pydantic import BaseModel
from datetime import datetime
from backend.helpers.forms import ValidateJsonWithFormBody
from backend.schemas.ideas import Idea
from backend.schemas.user import UserInfo
from fastapi import Query
from backend.core.config import env_config

class PostCreateBase(BaseModel):
    title: str
    description: str
    url: str


class CreatePost(PostCreateBase, ValidateJsonWithFormBody):
    idea_id: int


class PostBase(PostCreateBase):
    id: int
    user_id: int
    time_created: datetime
    picture: str
    likes: int
    liked: bool


class PostWithUser(PostBase):
    user: UserInfo
    idea_id: int


class PostUserWithIdea(PostWithUser):
    idea: Idea


class PostWithIdea(PostBase):
    idea: Idea

class CreateComment(BaseModel):
    text: str = Query(..., max_length=int(env_config.get("VITE_MAX_POST_COMMENT_LENGTH")), min_length=int(env_config.get("VITE_MIN_POST_COMMENT_LENGTH")))