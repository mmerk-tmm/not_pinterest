from typing import List, Union
from fastapi import File, HTTPException, Depends, APIRouter, UploadFile, status, Query
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_idea import IdeaCRUD
from backend.crud.crud_keyword import KeywordCRUD
from backend.crud.crud_post import PostCRUD
from backend.crud.crud_user import UserCRUD
from backend.helpers.auth_helper import validate_authorized_user
from backend.helpers.ideas import set_idea_data
from backend.helpers.images import save_image
from backend.helpers.posts_helpers import get_post_json
from backend.responses import AUTH_REQUIRED_401, IDEA_WITH_THIS_NAME_ALREADY_EXISTS_400
from backend.schemas.ideas import CreateIdea, Idea, IdeaWithLike, IdeaWithUser, IdeaWithUserAndLike
from pydantic import parse_obj_as
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.db.db import get_db
from fastapi.encoders import jsonable_encoder

from backend.schemas.post import CreatePost, PostBase
router = APIRouter(tags=['Идеи'], prefix='/ideas')


@router.post('', response_model=Idea, responses={**IDEA_WITH_THIS_NAME_ALREADY_EXISTS_400, **AUTH_REQUIRED_401}, status_code=status.HTTP_201_CREATED)
def create_idea(idea_data: CreateIdea,  Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    idea_cruds = IdeaCRUD(db)
    if idea_cruds.get_idea_by_name(name=idea_data.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Идея с таким именем уже существует")
    db_idea = idea_cruds.create_idea(
        name=idea_data.name, description=idea_data.description, user_id=current_user_id)
    return set_idea_data(idea=db_idea, db=db, user_id=current_user_id)


@router.post('/{idea_id}/post', response_model=PostBase)
def create_post(idea_id: int, post_data: CreatePost, post_image: UploadFile = File(...),
                Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    db_user = validate_authorized_user(Authorize, db)
    db_idea = IdeaCRUD(db).get_idea_by_id(idea_id=idea_id)
    if not db_idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Идея не найдена")
    keywords_ids = []
    for keyword in post_data.keywords:
        db_keyword = KeywordCRUD(db).get_keyword_by_name(keyword)
        if not db_keyword:
            db_keyword = KeywordCRUD(db).create_keyword(keyword)
        keywords_ids.append(db_keyword.id)
    db_image = save_image(upload_file=post_image, db=db,
                          user_id=db_user.id)
    db_post = PostCRUD(db).create_post(
        title=post_data.title,
        description=post_data.description,
        url=post_data.url,
        user_id=db_user.id,
        db_picture=db_image,
        idea_id=idea_id
    )
    return db_post


@router.post('/{idea_id}/like', response_model=bool)
def like_post(idea_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    idea_cruds = IdeaCRUD(db)
    if not idea_cruds.get_idea_by_id(idea_id=idea_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Идея не найдена")
    db_idea = idea_cruds.toggle_like_idea(
        user_id=current_user_id, idea_id=idea_id)
    return db_idea


@router.get('', response_model=List[Union[IdeaWithUser, IdeaWithUserAndLike]])
def get_ideas(page: int = 1, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_optional()
    current_user_id = Authorize.get_jwt_subject()
    idea_cruds = IdeaCRUD(db)
    db_ideas = idea_cruds.get_ideas(page=page)
    ideas = [set_idea_data(idea=idea, user_id=current_user_id, db=db)
             for idea in db_ideas]
    return JSONResponse(jsonable_encoder(parse_obj_as(List[IdeaWithUserAndLike if current_user_id else IdeaWithUser], ideas)))


@router.delete('/{idea_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_idea(idea_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = UserCRUD(db)
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неправильное имя пользователя или пароль")
    idea_cruds = IdeaCRUD(db)
    idea = idea_cruds.get_idea_by_id(idea_id=idea_id)
    if not idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Идея не найдена")
    if not db_user.is_superuser or idea.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Вы не можете удалить эту идею")
    idea_cruds.delete(model=idea)
