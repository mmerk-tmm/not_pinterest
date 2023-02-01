from backend.crud.crud_file import FileCRUD
from backend.db.base import CRUDBase
from backend.models.files import Image
from backend.schemas.user import UserModifiable, UserRegister
from backend.models.user import PersonalInformation, User
from fastapi.encoders import jsonable_encoder


class UserCRUD(CRUDBase):
    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_personal_information(self, user_id: int) -> PersonalInformation | None:
        return self.db.query(PersonalInformation).filter(PersonalInformation.user_id == user_id).first()

    def update_personal_information(self, user_id: int, gender: str):
        personal_information = self.get_personal_information(user_id)
        if not personal_information:
            return self.create(PersonalInformation(user_id=user_id, gender=gender))
        personal_information.gender = gender
        return self.create(personal_information)

    def update_user(self, user: User, new_user_data: UserModifiable, userPic: Image) -> User:
        if user is None:
            raise Exception('Update user failed: user is None')
        data_obj = new_user_data.dict()
        remove_picture = data_obj.pop('remove_picture')
        for var, value in data_obj.items():
            setattr(user, var, value)
        if remove_picture:
            self.delete(user.picture)
        elif userPic:
            FileCRUD(self.db).replace_old_picture(
                model=user, new_picture=userPic)
        return self.create(user)

    def is_admin(self, user_id):
        db_user = self.get_user_by_id(user_id=user_id)
        if not db_user:
            raise Exception('Пользователь не найден')
        return db_user.is_superuser
