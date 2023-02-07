from typing import List
from fastapi import APIRouter
from fastapi import HTTPException, status
from backend.crud.crud_comments import CommentCRUD
from backend.crud.crud_post import PostCRUD
from backend.crud.crud_user import UserCRUD
from backend.helpers.images import save_image
from backend.helpers.posts_helpers import get_post_json
from backend.schemas.post import CreateComment, CreatePost, PostComment, PostCreateBase, PostUserWithIdea,  PostBase
from fastapi import Depends, APIRouter, status, UploadFile, File, HTTPException
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import Session
from backend.db.db import get_db

router = APIRouter(tags=['Комментарии'], prefix='/comments')

@router.put('/{comment_id}', response_model=PostComment)
def update_comment(comment_id: int, comment_data: CreateComment, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    comment_cruds = CommentCRUD(db)
    comment = comment_cruds.get_comment_by_id(comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Комментарий не найден")
    if comment.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Вы не можете изменить чужой комментарий")
    return comment_cruds.update_comment(db_comment=comment, text=comment_data.text)

@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    comment_cruds = CommentCRUD(db)
    comment = comment_cruds.get_comment_by_id(comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Комментарий не найден")
    if comment.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Вы не можете удалить чужой комментарий")
    comment_cruds.delete_comment(db_comment=comment)
