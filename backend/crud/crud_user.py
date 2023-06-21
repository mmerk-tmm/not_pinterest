from backend.crud.crud_file import FileCRUD
from backend.db.base import CRUDBase
from backend.models.files import Image
from backend.schemas.schemas import UserModifiable, UserRegister
from backend.models.user import PersonalInformation, User, UserLike
from fastapi.encoders import jsonable_encoder
from backend.crud.crud_file import FileCRUD


class UserCRUD(CRUDBase):
    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_followed_users(self, user_id: int, page: int, page_size: int = 30):
        end = page * page_size
        return (
            self.db.query(User)
            .join(UserLike, UserLike.liked_user_id == User.id)
            .filter(UserLike.user_id == user_id)
            .order_by(User.id.desc())
            .slice(end - page_size, end)
            .all()
        )

    def toggle_like_user(self, user_id: int, user_liking_id: int):
        like = (
            self.db.query(UserLike)
            .filter(
                UserLike.user_id == user_liking_id, UserLike.liked_user_id == user_id
            )
            .first()
        )
        if like:
            self.db.delete(like)
            self.db.commit()
            return False
        else:
            self.create(
                UserLike(user_id=user_liking_id, liked_user_id=user_id))
            self.db.commit()
            return True

    def update_user_avatar(self, user: User, userPic: Image) -> User:
        if user is None:
            raise Exception("Update user failed: user is None")
        if userPic and user.picture:
            print("set new picture with deleting old")
            FileCRUD(self.db).replace_old_picture(
                model=user, new_picture=userPic)
        elif userPic:
            user.picture_id = userPic.id
            print("set new picture without deleting old", user.picture_id)
        elif user.picture:
            print("delete old picture")
            self.delete(user.picture)

        return self.update(user)

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_personal_information(self, user_id: int) -> PersonalInformation | None:
        return (
            self.db.query(PersonalInformation)
            .filter(PersonalInformation.user_id == user_id)
            .first()
        )

    def update_personal_information(self, user_id: int, gender: str):
        personal_information = self.get_personal_information(user_id)
        if not personal_information:
            return self.create(PersonalInformation(user_id=user_id, gender=gender))
        personal_information.gender = gender
        return self.create(personal_information)

    def update_user(self, user: User, new_user_data: UserModifiable) -> User:
        if user is None:
            raise Exception("Update user failed: user is None")
        data_obj = new_user_data.dict()

        for var, value in data_obj.items():
            setattr(user, var, value)
        return self.create(user)

    def is_admin(self, user_id):
        db_user = self.get_user_by_id(user_id=user_id)
        if not db_user:
            raise Exception("Пользователь не найден")
        return db_user.is_superuser
