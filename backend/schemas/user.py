from typing import List
from pydantic import BaseModel
from core.config import settings
from schemas.file import File
from helpers.forms import form_body


class UserAuth(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None


class UserTypes(BaseModel):
    is_superuser: bool = False


class UserWithTypeRegister(UserBase, UserAuth, UserTypes):
    ...


class UserRegister(UserBase, UserAuth):
    ...


class UserModifiable(UserBase):
    ...


@form_body
class UserModifiableForm(UserBase):
    ...
    remove_picture: bool = False


class UserInfo(UserTypes, UserBase):
    id: int
    username: str
    picture: str | None = None