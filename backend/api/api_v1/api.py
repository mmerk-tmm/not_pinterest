from fastapi import APIRouter
from backend.api.api_v1.endpoints import auth, user, files, ideas, posts, comments, keywords, search

api_v1_router = APIRouter()
api_v1_router.include_router(auth.router)
api_v1_router.include_router(user.router)
api_v1_router.include_router(files.router)
api_v1_router.include_router(ideas.router)
api_v1_router.include_router(posts.router)
api_v1_router.include_router(comments.router)
api_v1_router.include_router(keywords.router)
api_v1_router.include_router(search.router)
