from datetime import datetime
from pydantic import BaseModel


class CreateIdea(BaseModel):
    name: str
    description: str


class Idea(CreateIdea):
    id: int
    created: str
    likes: int
