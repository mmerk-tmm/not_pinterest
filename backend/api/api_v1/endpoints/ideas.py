from typing import List, Union
from fastapi import HTTPException, Depends, APIRouter, status, Query
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_idea import IdeaCRUD
from backend.crud.crud_user import UserCRUD
from backend.helpers.ideas import set_idea_data
from backend.responses import AUTH_REQUIRED_401, IDEA_WITH_THIS_NAME_ALREADY_EXISTS_400
from backend.schemas.ideas import CreateIdea, Idea, IdeaWithLike, IdeaWithUser, IdeaWithUserAndLike
from pydantic import parse_obj_as
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.db.db import get_db
from fastapi.encoders import jsonable_encoder
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
    idea=idea_cruds.get_idea_by_id(idea_id=idea_id)
    if not idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Идея не найдена")
    if not db_user.is_superuser or idea.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Вы не можете удалить эту идею")
    idea_cruds.delete(model=idea)