from typing import Any
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi_jwt_auth import AuthJWT
from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.schemas.schemas import UserAuth, UserInfo
from backend.crud.crud_user import UserCRUD
from backend.crud.crud_auth import AuthCRUD
from backend.schemas.schemas import UserRegister
from backend.db.db import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Авторизация"], prefix="/auth")


@router.post(
    "/login",
    response_model=UserInfo,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}},
)
def login(
    user_in: UserAuth, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)
):
    db_user = AuthCRUD(db).login(user_in)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="неправильное имя пользователя или пароль",
        )
    access_token = Authorize.create_access_token(subject=db_user.id)
    refresh_token = Authorize.create_refresh_token(subject=db_user.id)
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return db_user


@router.delete("/logout")
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}


@router.post("/refresh")
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user_id = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user_id)
    Authorize.set_access_cookies(new_access_token)
    return {"msg": "The token has been refresh"}


@router.post("/signup", response_model=UserInfo, status_code=201)
def create_user_signup(
    user_in: UserRegister, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)
) -> Any:
    """
    Создание пользователя без необходимости последующей авторизации
    """
    user_exists = UserCRUD(db).get_user_by_username(user_in.username)
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="Такой пользователь уже существует",
        )
    db_user = AuthCRUD(db).create_user(user_in)
    access_token = Authorize.create_access_token(subject=db_user.id)
    refresh_token = Authorize.create_refresh_token(subject=db_user.id)
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return db_user
