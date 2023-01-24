from fastapi import Depends, APIRouter, status, UploadFile, File, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.helpers.images import save_image
from backend.helpers.images import set_picture
from backend.responses import AUTH_REQUIRED_401, UNAUTHORIZED_401
from backend.schemas.user import PersonalInformation, PersonalInformationBase, UserInfo, UserModifiableForm
from backend.crud.crud_user import user_cruds
router = APIRouter(tags=['Профили пользователей'], prefix='/users')


@router.put('/me', responses={**UNAUTHORIZED_401}, response_model=UserInfo)
def update_user_data(UserData: UserModifiableForm = Depends(UserModifiableForm), userPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    db_image = save_image(upload_file=userPicture,
                         user_id=db_user.id)
    if UserData.username:
        db_user_username = user_cruds.get_user_by_username(
            username=UserData.username)
        if db_user_username and db_user_username.id != current_user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="пользователь с таким юзернеймом уже существует")
    db_user_updated = user_cruds.update(
        user=db_user, new_user_data=UserData, userPic=db_image)
    user_data = db_user_updated.as_dict()
    user_data = set_picture(user_data, db_user_updated.picture)
    return user_data


@router.put('/me/personal-information', responses={**UNAUTHORIZED_401}, response_model=PersonalInformation)
def update_user_data(UserData: PersonalInformationBase, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    return user_cruds.update_personal_information(user_id=current_user_id, gender=UserData.gender).as_dict()


@router.get('/me/personal-information', responses={**UNAUTHORIZED_401}, response_model=PersonalInformation)
def update_user_data(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    personal_information = user_cruds.get_personal_information(
        user_id=current_user_id)
    if not personal_information:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Персональные данные не заданы")
    return personal_information.as_dict()


@router.get('/me', responses={**AUTH_REQUIRED_401}, response_model=UserInfo)
def get_user_info(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user = user_cruds.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Необходимо авторизоваться")
    user_data = user.as_dict()
    user_data = set_picture(user_data, user.picture)
    return user_data
