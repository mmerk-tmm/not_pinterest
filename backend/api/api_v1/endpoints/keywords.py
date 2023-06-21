from typing import List
from fastapi import APIRouter
from fastapi import HTTPException, status
from backend.crud.crud_keyword import KeywordCRUD
from backend.schemas.schemas import Keyword
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi_jwt_auth import AuthJWT
from backend.helpers.auth_helper import Authenticate
from sqlalchemy.orm import Session
from backend.db.db import get_db

router = APIRouter(tags=["Ключевые слова"], prefix="/keywords")


@router.get("/search", response_model=List[Keyword])
def search_keyword(keyword: str, Auth: Authenticate = Depends(Authenticate())):
    keywords = KeywordCRUD(Auth.db).search_keywords(name=keyword)
    keywords_objs = []
    for keyword in keywords:
        keyword_obj = Keyword.from_orm(keyword)
        if Auth.current_user_id:
            keyword_obj.liked = bool(
                KeywordCRUD(Auth.db).get_keyword_like_by_user_id(
                    keyword_id=keyword.id, user_id=Auth.current_user_id
                )
            )
        keywords_objs.append(keyword_obj)
    return keywords_objs


@router.get("", response_model=List[Keyword])
def get_keywords(page: int = 1, Auth: Authenticate = Depends(Authenticate())):
    keywords = KeywordCRUD(Auth.db).get_keywords(page)
    keywords_objs = []
    for keyword in keywords:
        keyword_obj = Keyword.from_orm(keyword)
        if Auth.current_user_id:
            keyword_obj.liked = bool(
                KeywordCRUD(Auth.db).get_keyword_like_by_user_id(
                    keyword_id=keyword.id, user_id=Auth.current_user_id
                )
            )
        keywords_objs.append(keyword_obj)
    return keywords_objs


@router.get("/{keyword_id}", response_model=Keyword)
def get_keyword_by_id(
    keyword_id: int, Auth: Authenticate = Depends(Authenticate(required=False))
):
    keyword = KeywordCRUD(Auth.db).get_keyword_by_id(keyword_id=keyword_id)
    if not keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ключевое слово не найдено"
        )
    keyword_obj = Keyword.from_orm(keyword)
    if Auth.current_user_id:
        keyword_obj.liked = bool(
            KeywordCRUD(Auth.db).get_keyword_like_by_user_id(
                keyword_id=keyword_id, user_id=Auth.current_user_id
            )
        )
    return keyword


@router.delete("/{keyword_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_keyword_by_id(
    keyword_id: int, Auth: Authenticate = Depends(Authenticate(is_admin=True))
):
    keyword = KeywordCRUD(Auth.db).get_keyword_by_id(keyword_id=keyword_id)
    if not keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ключевое слово не найдено"
        )
    KeywordCRUD(Auth.db).delete_keyword(keyword=keyword)
