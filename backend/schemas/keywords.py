from pydantic import BaseModel
from backend.core.config import env_config
from fastapi import Query


class KeywordCreate(BaseModel):
    name: str = Query(
        ...,
        min_length=1,
        max_length=int(env_config.get('VITE_MAX_KEYWORD_NAME_LENGTH'))
    )

    class Config:
        orm_mode = True


class Keyword(KeywordCreate):
    id: int
    liked: bool = False

    class Config:
        orm_mode = True
