from typing import List
from fastapi import APIRouter
from fastapi import HTTPException, status
from backend.crud.crud_post import PostCRUD
from backend.crud.crud_user import UserCRUD
from backend.crud.crud_keyword import KeywordCRUD
from backend.helpers.images import save_image
from backend.helpers.posts_helpers import get_post_json
from backend.schemas.post import CreateComment, CreatePost, PostComment, PostCreateBase, PostUserWithIdea,  PostBase
from fastapi import Depends, APIRouter, status, UploadFile, File, HTTPException
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi_jwt_auth import AuthJWT
from backend.helpers.auth_helper import Authenticate

from sqlalchemy.orm import Session
from backend.db.db import get_db
router = APIRouter(tags=['Посты'], prefix='/posts')


@router.get('/last', response_model=List[PostUserWithIdea])
def get_posts(page: int = 1, Auth: Authenticate = Depends(Authenticate(required=False))):
    posts = PostCRUD(Auth.db).get_posts(page=page)
    posts_objs = []
    for post in posts:
        post_obj = PostUserWithIdea.from_orm(post)
        if Auth.current_user_id:
            post_obj.liked = bool(PostCRUD(Auth.db).get_post_like_by_user_id(
                post_id=post.id, user_id=Auth.current_user_id))
        posts_objs.append(post_obj)
    return posts_objs


@router.get('/{post_id}', response_model=PostUserWithIdea)
def get_post(post_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_optional()
    post = PostCRUD(db).get_post_by_id(post_id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пост не найден")
    return post


@router.put('/{post_id}', response_model=PostBase)
def update_post(post_id: int, post_data: PostCreateBase,
                Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = UserCRUD(db)
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    post_cruds = PostCRUD(db)
    db_post = post_cruds.get_post_by_id(post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пост не найден")
    if db_post.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Вы не можете редактировать этот пост")
    db_post = post_cruds.update_post(
        db_post=db_post,
        title=post_data.title,
        description=post_data.description,
        url=post_data.url,
    )
    db_post_obj = get_post_json(
        post=db_post, current_user_id=current_user_id, db=db)
    return db_post_obj


@router.put('/{post_id}/like', response_model=bool)
def like_post(post_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = UserCRUD(db)
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    post_cruds = PostCRUD(db)
    db_post = post_cruds.get_post_by_id(post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пост не найден")
    is_liked = post_cruds.toggle_like_post(
        post_id=post_id,
        user_id=current_user_id
    )
    return is_liked


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = UserCRUD(db)
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неправильное имя пользователя или пароль")
    post_cruds = PostCRUD(db)
    db_post = post_cruds.get_post_by_id(post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пост не найден")
    if db_post.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Вы не можете редактировать этот пост")
    post_cruds.delete_post(db_post=db_post)


@router.post('/{post_id}/comments', response_model=PostComment)
def create_post_comment(post_id: int, post_data: CreateComment, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = UserCRUD(db)
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неправильное имя пользователя или пароль")
    post_cruds = PostCRUD(db)
    db_post = post_cruds.get_post_by_id(post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пост не найден")
    return post_cruds.create_comment(
        user_id=current_user_id, post=db_post, text=post_data.text
    )


@router.get('/{post_id}/comments', response_model=List[PostComment])
def get_post_comments(page: int, post_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = UserCRUD(db)
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неправильное имя пользователя или пароль")
    post_cruds = PostCRUD(db)
    db_post = post_cruds.get_post_by_id(post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пост не найден")
    return post_cruds.get_comments(post_id=post_id, page=page)
