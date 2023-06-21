from fastapi import Depends, APIRouter, status, UploadFile, File, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.helpers.auth_helper import Authenticate
from backend.helpers.images import save_image
from backend.helpers.images import set_picture
from backend.responses import AUTH_REQUIRED_401, UNAUTHORIZED_401
from backend.schemas.schemas import UserWithPosts
from backend.schemas.schemas import (
    PersonalInformation,
    PersonalInformationBase,
    UserInfo,
    UserInfoBase,
    UserModifiable,
    UserModifiableForm,
)
from backend.crud.crud_user import UserCRUD
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.crud.crud_post import PostCRUD

router = APIRouter(tags=["Профили пользователей"], prefix="/users")


@router.put("/me", responses={**UNAUTHORIZED_401}, response_model=UserInfoBase)
def update_user_data(
    UserData: UserModifiable,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = UserCRUD(db)
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="неправильное имя пользователя или пароль",
        )
    if UserData.username:
        db_user_username = user_cruds.get_user_by_username(username=UserData.username)
        if db_user_username and db_user_username.id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="пользователь с таким юзернеймом уже существует",
            )
    db_user_updated = user_cruds.update_user(user=db_user, new_user_data=UserData)
    db_user_updated.current_user_id = current_user_id
    return db_user_updated


@router.put(
    "/me/avatar",
    response_model=UserInfo,
)
def update_user_avatar(
    Auth: Authenticate = Depends(Authenticate()),
    userPicture: UploadFile = File(default=False, description="Фото пользователя"),
):
    """Обновление данных пользователя"""
    db_image = save_image(
        db=Auth.db, upload_file=userPicture, user_id=Auth.current_user.id
    )
    db_user_updated = UserCRUD(Auth.db).update_user_avatar(
        user=Auth.current_user,
        userPic=db_image,
    )
    return db_user_updated


@router.put(
    "/me/personal-information",
    responses={**UNAUTHORIZED_401},
    response_model=PersonalInformation,
)
def update_user_data(
    UserData: PersonalInformationBase,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = UserCRUD(db)
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="неправильное имя пользователя или пароль",
        )
    return user_cruds.update_personal_information(
        user_id=current_user_id, gender=UserData.gender
    ).as_dict()


@router.get(
    "/me/personal-information",
    responses={**UNAUTHORIZED_401},
    response_model=PersonalInformation,
)
def update_user_data(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = UserCRUD(db)
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="неправильное имя пользователя или пароль",
        )
    personal_information = user_cruds.get_personal_information(user_id=current_user_id)
    if not personal_information:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Персональные данные не заданы",
        )
    return personal_information.as_dict()


@router.get("/me", responses={**AUTH_REQUIRED_401}, response_model=UserInfoBase)
def get_user_info(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = UserCRUD(db)
    user = user_cruds.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Необходимо авторизоваться"
        )
    return user


@router.get("/{user_id}", response_model=UserWithPosts)
def get_user_posts(
    user_id: int, page: int, Auth: Authenticate = Depends(Authenticate(required=False))
):
    db_user = UserCRUD(Auth.db).get_user_by_id(user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    db_user.posts_page = page
    db_user.current_user_id = Auth.current_user.id
    return db_user


@router.put("/{user_id}/like", response_model=bool)
def like_user(user_id: int, Auth: Authenticate = Depends(Authenticate())):
    db_user = UserCRUD(Auth.db).get_user_by_id(user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return UserCRUD(Auth.db).toggle_like_user(
        user_id=user_id, user_liking_id=Auth.current_user.id
    )
