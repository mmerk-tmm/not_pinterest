from typing import List, Union
from fastapi import File, HTTPException, Depends, APIRouter, Path, UploadFile, status
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_idea import IdeaCRUD
from backend.crud.crud_keyword import KeywordCRUD
from backend.crud.crud_post import PostCRUD
from backend.crud.crud_user import UserCRUD
from backend.helpers.auth_helper import Authenticate
from backend.helpers.ideas import set_idea_data
from backend.helpers.images import save_image
from backend.responses import AUTH_REQUIRED_401, IDEA_WITH_THIS_NAME_ALREADY_EXISTS_400
from backend.schemas.ideas import CreateIdea, Idea,  IdeaWithUserAndLike
from sqlalchemy.orm import Session
from backend.db.db import get_db

from backend.schemas.post import CreatePost, PostBase
router = APIRouter(tags=['Идеи'], prefix='/ideas')


@router.get('/search', response_model=List[IdeaWithUserAndLike])
def search_ideas(query: str, Auth: Authenticate = Depends(Authenticate(required=False))):
    db_ideas = IdeaCRUD(Auth.db).search_ideas(query=query)
    db_ideas_objs = []
    for db_idea in db_ideas:
        db_idea_obj = IdeaWithUserAndLike.from_orm(db_idea)
        if Auth.current_user_id:
            db_idea_obj.liked = bool(IdeaCRUD(Auth.db).get_idea_like_by_user_id(
                idea_id=db_idea.id, user_id=Auth.current_user_id))
        db_ideas_objs.append(db_idea_obj)
    return db_ideas


@router.post('', response_model=Idea, responses={**IDEA_WITH_THIS_NAME_ALREADY_EXISTS_400, **AUTH_REQUIRED_401}, status_code=status.HTTP_201_CREATED)
def create_idea(idea_data: CreateIdea,  Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    idea_cruds = IdeaCRUD(db)
    if idea_cruds.get_idea_by_name(name=idea_data.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Идея с таким именем уже существует")
    keywords = []
    for keyword in idea_data.keywords_ids:
        db_keyword = KeywordCRUD(db).get_keyword_by_id(keyword)
        if not db_keyword:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Ключевое слово не найдено")
        keywords.append(db_keyword)
    for keyword in idea_data.new_keywords:
        db_keyword = KeywordCRUD(db).get_keyword_by_name(keyword)
        if not db_keyword:
            db_keyword = KeywordCRUD(db).create_keyword(keyword)
        keywords.append(db_keyword)

    db_idea = idea_cruds.create_idea(
        name=idea_data.name, description=idea_data.description, user_id=current_user_id, keywords=keywords)
    return db_idea


@router.post('/{idea_id}/post', response_model=PostBase)
def create_post(
    post_data: CreatePost,
    idea_id: int = Path(..., title="Идентификатор идеи", ge=1),
    post_image: UploadFile = File(...),
    Auth: Authenticate = Depends(Authenticate())
):

    db_idea = IdeaCRUD(Auth.db).get_idea_by_id(idea_id=idea_id)
    if not db_idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Идея не найдена")
    keywords = []
    for keyword in post_data.keywords:
        db_keyword = KeywordCRUD(Auth.db).get_keyword_by_name(keyword)
        if not db_keyword:
            db_keyword = KeywordCRUD(Auth.db).create_keyword(keyword)
        keywords.append(db_keyword)
    db_image = save_image(upload_file=post_image, db=Auth.db,
                          user_id=Auth.current_user_id)
    db_post = PostCRUD(Auth.db).create_post(
        title=post_data.title,
        description=post_data.description,
        url=post_data.url,
        user_id=Auth.current_user_id,
        db_picture=db_image,
        idea_id=idea_id,
        keywords=keywords
    )
    return db_post


@router.post('/{idea_id}/like', response_model=bool)
def like_post(idea_id: int, Auth: Authenticate = Depends(Authenticate())):
    idea_cruds = IdeaCRUD(Auth.db)
    if not idea_cruds.get_idea_by_id(idea_id=idea_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Идея не найдена")
    db_idea = idea_cruds.toggle_like_idea(
        user_id=Auth.current_user_id, idea_id=idea_id)
    return db_idea


@router.get('', response_model=List[IdeaWithUserAndLike])
def get_ideas(page: int = 1, Auth: Authenticate = Depends(Authenticate(required=False))):
    idea_cruds = IdeaCRUD(Auth.db)
    db_ideas = idea_cruds.get_ideas(page=page)
    db_ideas_objs = []
    for db_idea in db_ideas:
        db_idea_obj = IdeaWithUserAndLike.from_orm(db_idea)
        if Auth.current_user_id:
            db_idea_obj.liked = bool(idea_cruds.get_idea_like_by_user_id(
                idea_id=db_idea.id, user_id=Auth.current_user_id))
        db_ideas_objs.append(db_idea_obj)
    return db_ideas


@router.delete('/{idea_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_idea(idea_id: int, Auth: Authenticate = Depends(Authenticate())):
    idea_cruds = IdeaCRUD(Auth.db)
    idea = idea_cruds.get_idea_by_id(idea_id=idea_id)
    if not idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Идея не найдена")
    if not Auth.current_user.is_superuser or idea.user_id != Auth.current_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Вы не можете удалить эту идею")
    idea_cruds.delete(model=idea)
