import pytest
from fastapi.testclient import TestClient
from tests.utils.names import generate_random_name
from backend.core.config import env_config

# def test_create_idea(client: TestClient, normal_user_token_headers):
#     data = {"title": "Test idea", "description": "Test idea description"}
#     response = client.post("/ideas/", headers=normal_user_token_headers, json=data)
#     assert response.status_code == 201
#     return response.json()


@pytest.mark.parametrize("input_data, expected_status_code", [
    ({"name": "Test idea", "description": "Test idea description"}, 201),
    # идея с таким названием уже существует
    ({"name": "Test idea", "description": "Test idea description"}, 400),
    ({"name": generate_random_name(int(
        env_config.get("VITE_MAX_IDEA_NAME_LENGTH")) + 1), "description": "Test idea description"}, 422),  # название идеи слишком длинное
    ({"name": generate_random_name(int(
        env_config.get("VITE_MIN_IDEA_NAME_LENGTH")) - 1), "description": "Test idea description"}, 422),  # название идеи слишком короткое
    ({"name": "Test idea", "description": generate_random_name(int(
        env_config.get("VITE_MAX_IDEA_DESCRIPTION_LENGTH")) + 1)}, 422),  # описание идеи слишком длинное

])
def test_create_idea(client: TestClient, normal_user_token_cookies, input_data: dict, expected_status_code: int):
    response = client.post(
        "/ideas/", headers=normal_user_token_cookies, json=input_data)
    print(response.json())
    assert response.status_code == expected_status_code
