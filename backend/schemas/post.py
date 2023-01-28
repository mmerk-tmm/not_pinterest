from pydantic import BaseModel
from datetime import datetime
from backend.helpers.forms import ValidateJsonWithFormBody
from backend.schemas.ideas import Idea
from backend.schemas.user import UserInfo


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
