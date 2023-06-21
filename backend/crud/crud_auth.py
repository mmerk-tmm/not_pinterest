from backend.crud.crud_user import UserCRUD
from backend.db.base import CRUDBase
from backend.schemas.schemas import UserAuth, UserRegister
from backend.models.user import User
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder


class AuthCRUD(CRUDBase):
    def __init__(self, db) -> None:
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def login(self, user: UserAuth) -> User | None:
        db_user = UserCRUD(self.db).get_user_by_username(username=user.username)
        if not db_user:
            return None
        if not self.pwd_context.verify(user.password, db_user.hashed_password):
            return None
        return db_user

    def create_user(self, user: UserRegister, admin=False) -> User:
        password_hash = self.pwd_context.hash(user.password)
        user_in_data = jsonable_encoder(user)
        del user_in_data["password"]
        db_user = User(
            hashed_password=password_hash,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            is_superuser=admin,
        )
        return self.create(db_user)
