from pydantic import BaseModel
from datetime import datetime


class CratePost(BaseModel):
    title: str
    description: str
    url: str
    idea_id: int


class Post(CratePost):
    id: int
    user_id: int
    time_created: datetime
    picture: str
