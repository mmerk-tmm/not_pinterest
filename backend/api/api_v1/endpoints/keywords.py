from typing import List
from fastapi import APIRouter
from fastapi import HTTPException, status
from backend.crud.crud_post import PostCRUD
from backend.crud.crud_user import UserCRUD
from backend.crud.crud_keyword import KeywordCRUD
from backend.helpers.images import save_image
from backend.helpers.posts_helpers import get_post_json
from backend.schemas.keywords import Keyword
from backend.schemas.post import CreatePost, PostComment, PostCreateBase, PostUserWithIdea,  PostBase
from fastapi import Depends, APIRouter, status, UploadFile, File, HTTPException
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi_jwt_auth import AuthJWT
from backend.helpers.auth_helper import validate_authorized_user

from sqlalchemy.orm import Session
from backend.db.db import get_db
router = APIRouter(tags=['Ключевые слова'], prefix='/keywords')


@router.get('', response_model=List[Keyword])
def get_keywords(db: Session = Depends(get_db)):
    keywords = PostCRUD(db).get_keywords()
    return keywords


@router.get('/{keyword_id}', response_model=Keyword)
def get_keyword_by_id(keyword_id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    current_user_id = Authorize.get_jwt_subject()
    keyword = KeywordCRUD(db).get_keyword_by_id(keyword_id=keyword_id)
    if not keyword:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Ключевое слово не найдено")
    keyword_obj = Keyword.from_orm(keyword)
    if current_user_id:
        keyword_obj.liked = bool(KeywordCRUD(db).get_keyword_like_by_user_id(
            keyword_id=keyword_id, user_id=current_user_id))
    return keyword


@router.delete('/{keyword_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_keyword_by_id(keyword_id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    validate_authorized_user(Authorize, db, is_admin=True)
    keyword = KeywordCRUD(db).get_keyword_by_id(keyword_id=keyword_id)
    if not keyword:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Ключевое слово не найдено")
    KeywordCRUD(db).delete_keyword(keyword=keyword)
