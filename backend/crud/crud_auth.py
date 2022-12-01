from backend.crud.crud_user import user_cruds
from backend.db.base import CRUDBase
from backend.schemas.user import UserAuth,  UserRegister
from backend.models.user import User
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder


class AuthCruds(CRUDBase):
    def __init__(self) -> None:
        super().__init__()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def login(self, user: UserAuth) -> User | None:
        db_user = user_cruds.get_user_by_username(username=user.username)
        if not db_user:
            return None
        if not self.pwd_context.verify(user.password, db_user.hashed_password):
            return None
        return db_user

    def create_user(self, user: UserRegister) -> User:
        password_hash = self.pwd_context.hash(user.password)
        user_in_data = jsonable_encoder(user)
        del user_in_data['password']
        db_user = User(hashed_password=password_hash, **user_in_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user


auth_cruds = AuthCruds()
