
from pydantic import BaseModel


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }


class HTTP_401_UNAUTHORIZED(BaseModel):
    detail: str = "неправильное имя пользователя или пароль"


class AUTH_REQUIRED(BaseModel):
    detail: str = "Необходимо авторизоваться"


class USER_NOT_FOUND(BaseModel):
    detail: str = "Пользователь не найден"


class NOT_ENOUGH_RIGHTS_403(BaseModel):
    detail: str = "Недостаточно прав"


class IDEA_WITH_THIS_NAME_ALREADY_EXISTS(BaseModel):
    detail: str = "Идея с таким именем уже существует"
