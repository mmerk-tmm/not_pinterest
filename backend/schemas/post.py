from pydantic import BaseModel
from datetime import datetime

class CratePost(BaseModel):
    title: str
    description: str
    url: str

class Post(CratePost):
    id: int
    user_id: int
    time_created: datetime
    idea_id: int