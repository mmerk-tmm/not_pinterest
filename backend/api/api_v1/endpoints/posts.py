from typing import List
from fastapi import APIRouter
from fastapi import HTTPException, status
from backend.crud.crud_post import post_cruds
from backend.crud.crud_user import user_cruds
from backend.helpers.images import save_image, set_picture
from backend.schemas.post import CratePost, Post
from fastapi import Depends, APIRouter, status, UploadFile, File, HTTPException
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
router = APIRouter(tags=['Посты'], prefix='/posts')


@router.get('')
def get_posts(page: int = 1):
    return post_cruds.get_posts(page=page)


@router.get('/{post_id}')
def get_post(post_id: int):
    post = post_cruds.get_post_by_id(post_id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пост не найден")
    return post


@router.post('', response_model=Post)
def create_post(post_data: CratePost = Depends(CratePost), post_image: UploadFile = File(...),
                Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    db_image = save_image(upload_file=post_image,
                          user_id=db_user.id)
    db_post = post_cruds.create_post(
        **post_data.dict(), user_id=current_user_id, db_picture=db_image)
    db_post_obj = jsonable_encoder(db_post)
    db_post_obj = set_picture(db_post_obj, db_image)
    return db_post_obj
