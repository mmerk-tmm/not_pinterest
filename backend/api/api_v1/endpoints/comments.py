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

router = APIRouter(tags=['Комметарии'], prefix='/comments')

@router.put('{comment_id}', response_model=PostComment)
def update_comment(comment_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    comment = CommentCRUD(db).get_comment_by_id(comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Комментарий не найден")
    return get_post_json(comment=comment, current_user_id=current_user_id, db=db)

@router.delete('{comment_id}/delete', response_model=PostComment)
def delete_comment(comment_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    comment = CommentCRUD(db).get_comment_by_id(comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Комментарий не найден")
    if comment.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Вы не можете удалить чужой комментарий")
    CommentCRUD(db).delete_comment(db_comment=comment)
    return get_post_json(comment=comment, current_user_id=current_user_id, db=db)

# Не работает, надо сделоть