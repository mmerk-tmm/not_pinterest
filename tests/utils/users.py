from fastapi.testclient import TestClient
from backend.crud.crud_user import UserCRUD
from backend.crud.crud_auth import AuthCRUD
from sqlalchemy.orm import Session
from backend.schemas.user import UserRegister
from backend.core.config import settings


def user_authentication_cookies(client: TestClient, username: str, password: str):
    user_data = UserRegister(username=username, password=password)
    response = client.post("/auth/login", json=user_data.dict())
    assert response.status_code == 200
    return response.cookies


def authentication_token_from_username(client: TestClient, username: str, db: Session, admin=False):
    password = "random-passW0rd"
    user = UserCRUD(db).get_user_by_username(username=username)
    if not user:
        user_data = UserRegister(username=username, password=password)
        user = AuthCRUD(db).create_user(user=user_data, admin=admin)
    return user_authentication_cookies(client=client, username=username, password=password)
