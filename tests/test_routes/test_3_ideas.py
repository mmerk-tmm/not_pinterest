import pytest
from fastapi.testclient import TestClient
from tests.utils.names import generate_random_name
from backend.core.config import env_config


def create_idea(client: TestClient, cookies: dict, input_data: dict, expected_status_code: int):
    response = client.post("/ideas", cookies=cookies, json=input_data)
    print(response.json())
    assert response.status_code == expected_status_code
    return response


@pytest.mark.parametrize("input_data, expected_status_code", [
    ({"name": "Test idea", "description": "Test idea description"}, 201),
    ({"name": "Test idea", "description": "Test idea description"}, 400),
    ({"name": generate_random_name(int(
        env_config.get("VITE_MAX_IDEA_NAME_LENGTH")) + 1), "description": "Test idea description"}, 422),  # название идеи слишком длинное
    ({"name": generate_random_name(int(
        env_config.get("VITE_MIN_IDEA_NAME_LENGTH")) - 1), "description": "Test idea description"}, 422),  # название идеи слишком короткое
    ({"name": "Test idea", "description": generate_random_name(int(
        env_config.get("VITE_MAX_IDEA_DESCRIPTION_LENGTH")) + 1)}, 422),  # описание идеи слишком длинное
])
def test_create_idea(client: TestClient, normal_user_token_cookies, input_data: dict, expected_status_code: int):
    create_idea(client, normal_user_token_cookies,
                input_data, expected_status_code)


def test_idea_like(client: TestClient, normal_user_token_cookies):
    idea = create_idea(client, normal_user_token_cookies,
                       {"name": generate_random_name(10), "description": "Test idea description"}, 201)
    response = client.post(
        f"/ideas/{idea.json()['id']}/like", cookies=normal_user_token_cookies)
    assert response.status_code == 200
    assert response.json() == True
    response = client.post(
        f"/ideas/{idea.json()['id']}/like", cookies=normal_user_token_cookies)
    assert response.status_code == 200
    assert response.json() == False
