from functools import wraps
from inspect import iscoroutinefunction
from typing import Callable, List
from fastapi import Depends, HTTPException, status
import fastapi
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from backend.crud.crud_user import UserCRUD
from backend.db.db import get_db
from backend.models.user import User
from backend.core.config import settings


class Authenticate:
    def __init__(
        self,
        is_admin: bool = False,
        required: bool = True,
    ):
        self.is_admin = is_admin
        self.required = required
        self.db = None
        self.current_user_id = None
        self.Authorize = None

    def __call__(self, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
        self.db = db
        self.current_user = None

        if self.required:
            try:
                Authorize.jwt_required()
                current_user_id = Authorize.get_jwt_subject()
            except:
                if self.required:
                    raise HTTPException(
                        status_code=403,
                        detail="Необходима авторизация"
                    )
                else:
                    return self
        else:
            try:
                Authorize.jwt_optional()
                current_user_id = Authorize.get_jwt_subject()
            except:
                current_user_id = None

        if not current_user_id and not self.required:
            return self
        db_user = UserCRUD(db).get_user_by_id(user_id=current_user_id)
        if not db_user:
            raise HTTPException(
                status_code=403,
                detail="Авторизованный пользователь не найден"
            )
        if self.is_admin and not db_user.is_superuser:
            raise HTTPException(
                status_code=403,
                detail=f"У вас недостаточно прав для выполнения этого действия, требуемый тип пользователя Администратор",
            )
        self.current_user = db_user
        self.current_user_id = current_user_id
        return self
