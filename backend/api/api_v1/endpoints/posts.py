from typing import List
from fastapi import APIRouter
from fastapi import HTTPException, status
from backend.crud.crud_post import post_cruds
from backend.models.post import Post
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi_jwt_auth import AuthJWT

router = APIRouter(tags=['Посты'], prefix='/posts')


@router.get('', response_model=List[Post])
def get_posts(page: int = 1):
    return post_cruds.get_posts(page=page)


@router.get('/{post_id}', response_model=Post)
def get_post(post_id: int):
    post = post_cruds.get_post_by_id(post_id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пост не найден")
    return post


@router.post('', response_model=Post)
def create_post(post_data: Post, post_image
                Authorize: AuthJWT = Depends()):
    return post_cruds.create_post(**post_data.dict())
