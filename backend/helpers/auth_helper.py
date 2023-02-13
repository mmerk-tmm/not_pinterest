from typing import List
from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from backend.crud.crud_user import UserCRUD
from backend.models.user import User
from backend.core.config import settings


def validate_authorized_user(Authorize: AuthJWT, db: Session, is_admin: bool = False) -> User:
    current_user_id = Authorize.get_jwt_subject()
    if not current_user_id:
        raise HTTPException(
            status_code=403,
            detail="Необходима авторизация"
        )
    db_user = UserCRUD(db).get_user_by_id(user_id=current_user_id)
    if not db_user:
        raise HTTPException(
            status_code=403,
            detail="Авторизованный пользователь не найден"
        )
    if is_admin and not db_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав"
        )
    return db_user
