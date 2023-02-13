from typing import List, Union
from pydantic import BaseModel
from datetime import datetime
from backend.helpers.forms import ValidateJsonWithFormBody
from backend.schemas.file import ImageLink
from backend.schemas.ideas import Idea
from backend.schemas.keywords import Keyword
from backend.schemas.user import UserInfo
from fastapi import Query
from backend.core.config import env_config


class PostCreateBase(BaseModel):
    title: str
    description: str
    url: str


class CreatePost(PostCreateBase, ValidateJsonWithFormBody):
    keywords: List[str]


class PostBase(PostCreateBase):
    id: int
    user_id: int
    time_created: datetime
    picture: ImageLink
    likes_count: int = 0
    liked: bool = False
    keywords: List[Keyword]

    class Config:
        orm_mode = True


class PostWithUser(PostBase):
    user: UserInfo
    idea_id: int


class PostUserWithIdea(PostWithUser):
    idea: Idea


class PostWithIdea(PostBase):
    idea: Idea


class CreateComment(BaseModel):
    text: str = Query(..., max_length=int(env_config.get("VITE_MAX_POST_COMMENT_LENGTH")),
                      min_length=int(env_config.get("VITE_MIN_POST_COMMENT_LENGTH")))


class PostComment(BaseModel):
    user_id: int
    id: int
    post_id: int
    content: str
    time_created: datetime
    time_edited: datetime

    class Config:
        orm_mode = True

# class PostCommentWithPostInformation(PostComment):
#     post: PostWithUser
