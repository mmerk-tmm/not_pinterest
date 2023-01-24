from typing import List, Union
from fastapi import HTTPException, Depends, APIRouter, status, Query
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_idea import idea_cruds
from backend.helpers.ideas import set_idea_data
from backend.schemas.ideas import CreateIdea, Idea, IdeaWithLike, Topic
from pydantic import parse_obj_as
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
router = APIRouter(tags=['Идеи'], prefix='/ideas')


@router.get('/search-topic', response_model=List[Topic])
def create_idea(name: str, limit: int = Query(gt=1, le=50, default=10)):
    return idea_cruds.search_topic(name=name, limit=limit)


@router.post('', response_model=Idea)
def create_idea(idea_data: CreateIdea,  Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    if idea_cruds.get_idea_by_name(name=idea_data.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Идея с таким именем уже существует")
    db_idea = idea_cruds.create_idea(
        name=idea_data.name, description=idea_data.description, user_id=current_user_id)
    return set_idea_data(idea=db_idea)


@router.post('/{idea_id}/like', response_model=bool)
def create_idea(idea_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    if not idea_cruds.get_idea_by_id(idea_id=idea_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Идея не найдена")
    db_idea = idea_cruds.toggle_like_idea(
        user_id=current_user_id, idea_id=idea_id)
    return db_idea


@router.get('', response_model=List[Union[Idea, IdeaWithLike]])
def get_ideas(page: int = 1, Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    current_user_id = Authorize.get_jwt_subject()
    db_ideas = idea_cruds.get_ideas(page=page)
    ideas = [set_idea_data(idea=idea, user_id=current_user_id)
             for idea in db_ideas]
    return JSONResponse(jsonable_encoder(parse_obj_as(List[IdeaWithLike if current_user_id else Idea], ideas)))
