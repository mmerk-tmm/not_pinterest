from typing import List
from fastapi import APIRouter
from fastapi import HTTPException, status
from backend.crud.crud_post import post_cruds
from backend.crud.crud_user import user_cruds
from backend.helpers.images import save_image, set_picture
from backend.helpers.posts_helpers import get_post_json
from backend.schemas.post import CreatePost, PostUserWithIdea, PostWithIdea
from fastapi import Depends, APIRouter, status, UploadFile, File, HTTPException
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
router = APIRouter(tags=['Посты'], prefix='/posts')


@router.get('', response_model=List[PostUserWithIdea])
def get_posts(page: int = 1, Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    current_user_id = Authorize.get_jwt_subject()
    posts = post_cruds.get_posts(page=page)
    return [get_post_json(post=post, current_user_id=current_user_id, idea_data=True, user_data=True) for post in posts]


@router.get('/{post_id}', response_model=PostUserWithIdea)
def get_post(post_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    current_user_id = Authorize.get_jwt_subject()
    post = post_cruds.get_post_by_id(post_id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пост не найден")
    return get_post_json(post=post, current_user_id=current_user_id)


@router.post('', response_model=PostWithIdea)
def create_post(post_data: CreatePost = Depends(CreatePost), post_image: UploadFile = File(...),
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
        title=post_data.title,
        description=post_data.description,
        url=post_data.url,
        user_id=current_user_id,
        db_picture=db_image
    )
    db_post_obj = get_post_json(post=db_post, current_user_id=current_user_id)
    return db_post_obj
