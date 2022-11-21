from typing import List
from pydantic import BaseModel, HttpUrl
from fastapi import Query
from backend.core.config import settings, env_config
from backend.schemas.file import File
from backend.helpers.forms import form_body


class UserUsername(BaseModel):
    username: str = Query(
        default=None,
        min_length=int(env_config.get('VITE_MIN_LOGIN_LENGTH')),
        max_length=int(env_config.get('VITE_MAX_LOGIN_LENGTH'))
    )


class UserAuth(UserUsername):
    password: str = Query(
        default=None,
        min_length=int(env_config.get('VITE_MIN_PASSWORD_LENGTH'))
    )


class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    description: str | None = None
    site: HttpUrl | None = None


class PersonalInformationBase(BaseModel):
    gender: str


class PersonalInformation(PersonalInformationBase):
    id: int
    user_id: int


class UserRegister(UserBase, UserAuth):
    ...


class UserModifiable(UserUsername, UserBase):
    ...


@form_body
class UserModifiableForm(UserModifiable):
    remove_picture: bool = False


class UserInfo(UserBase, UserUsername):
    id: int
    picture: str | None = None
