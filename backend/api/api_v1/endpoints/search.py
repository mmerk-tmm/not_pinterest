from typing import List, Union
from fastapi import File, HTTPException, Depends, APIRouter, Path, UploadFile, status
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_idea import IdeaCRUD
from backend.crud.crud_keyword import KeywordCRUD
from backend.crud.crud_post import PostCRUD
from backend.crud.crud_search import SearchCRUD

from backend.helpers.auth_helper import Authenticate

from backend.schemas.schemas import AllSearchItems


from backend.schemas.schemas import CreatePost, PostBase

router = APIRouter(tags=["Поиск"], prefix="/search")


@router.get("", response_model=List[AllSearchItems])
def search_all(
    query: str, Auth: Authenticate = Depends(Authenticate(required=False))
):
    return SearchCRUD(Auth.db).search_all(query=query)
