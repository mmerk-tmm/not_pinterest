from typing import List, Union
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from backend.helpers.forms import ValidateJsonWithFormBody, form_body

from backend.helpers.images import image_id_to_url

from backend.models.files import Image
from fastapi import Query
from backend.core.config import env_config


class File(BaseModel):
    file_name: str
    user_id: int
    type: str
    url: str
    original_file_name: str


class ImageLink(BaseModel):
    """convert relationship to image link"""

    @classmethod
    def get_validators(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Image):
        if not v:
            return None
        if isinstance(v, str):
            return v
        if not isinstance(v, Image):
            raise TypeError("ImageLink must be Image (model)")
        return image_id_to_url(v.id)


class UserUsername(BaseModel):
    username: str = Query(
        ...,
        min_length=int(env_config.get("VITE_MIN_LOGIN_LENGTH")),
        max_length=int(env_config.get("VITE_MAX_LOGIN_LENGTH")),
    )


class UserAuth(UserUsername):
    password: str = Query(
        ..., min_length=int(env_config.get("VITE_MIN_PASSWORD_LENGTH"))
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


class UserInfoBase(UserBase, UserUsername):
    id: int
    picture: ImageLink | None = None

    class Config:
        orm_mode = True


class UserInfo(UserInfoBase):
    followers_count: int
    liked: bool = False

    class Config:
        orm_mode = True


class PostCreateBase(BaseModel):
    title: str
    description: str
    url: str


class CreatePost(PostCreateBase, ValidateJsonWithFormBody):
    keywords: List[str]


class CreateComment(BaseModel):
    text: str = Query(
        ...,
        max_length=int(env_config.get("VITE_MAX_POST_COMMENT_LENGTH")),
        min_length=int(env_config.get("VITE_MIN_POST_COMMENT_LENGTH")),
    )


class PostComment(BaseModel):
    id: int
    post_id: int
    content: str
    time_created: datetime
    time_edited: datetime
    user: UserInfo

    class Config:
        orm_mode = True


class KeywordCreate(BaseModel):
    name: str = Query(
        ...,
        min_length=1,
        max_length=int(env_config.get("VITE_MAX_KEYWORD_NAME_LENGTH")),
    )

    class Config:
        orm_mode = True


class Keyword(KeywordCreate):
    id: int
    liked: bool = False

    class Config:
        orm_mode = True


class PostIdBase(PostCreateBase):
    picture: ImageLink
    id: int

    class Config:
        orm_mode = True


class PostBase(PostIdBase):
    id: int
    user_id: int
    time_created: datetime
    likes_count: int = 0
    liked: bool = False
    keywords: List[Keyword]
    comments: List[PostComment]

    class Config:
        orm_mode = True


class BaseIdea(BaseModel):
    name: str = Query(
        ...,
        max_length=int(env_config.get("VITE_MAX_IDEA_NAME_LENGTH")),
        min_length=int(env_config.get("VITE_MIN_IDEA_NAME_LENGTH")),
    )
    description: str = Query(
        ..., max_length=int(env_config.get("VITE_MAX_IDEA_DESCRIPTION_LENGTH"))
    )


class CreateIdea(BaseIdea):
    ...
    keywords_ids: List[int]
    new_keywords: List[str]


class Idea(BaseIdea):
    id: int
    created: datetime
    likes: int
    keywords: List[Keyword]

    class Config:
        orm_mode = True


class IdeaWithUser(Idea):
    user: UserInfo

    class Config:
        orm_mode = True


class IdeaWithLike(Idea):
    liked: bool = False


class IdeaWithUserAndLike(IdeaWithUser, IdeaWithLike):
    class Config:
        orm_mode = True


class IdeaKeyword(BaseModel):
    id: int
    name: str
    uses: int


class PostWithUser(PostBase):
    user: UserInfo
    idea_id: int

    class Config:
        orm_mode = True


class IdeaWithPosts(Idea):
    posts: List[PostWithUser]

    class Config:
        orm_mode = True


class PostUserWithIdea(PostWithUser):
    idea: Idea

    class Config:
        orm_mode = True


class PostWithIdea(PostBase):
    idea: Idea


class UserWithPosts(UserInfo):
    posts: List[PostBase]

    class Config:
        orm_mode = True


class AllSearchItems(BaseModel):
    type: str
    info: Union[UserInfo, PostIdBase, IdeaWithUser]

    class Config:
        orm_mode = True
