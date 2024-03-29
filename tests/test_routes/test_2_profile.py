import json
from fastapi.testclient import TestClient
import pytest

from tests.utils.names import generate_random_name
files = {
    "userPicture":  open("tests/test_files/test-profile-avatar.jpg", "rb"),
}
user_data = {
    "username": "asdasdadadadadsa",
    "first_name": "test_name2",
    "last_name": "test_last_name2"
}


def test_get_me(client: TestClient, normal_user_token_cookies):
    response = client.get("/users/me", cookies=normal_user_token_cookies)
    assert response.status_code == 200
    return response.json()


@pytest.mark.parametrize("input_data, files, expected_status_code", [
    ({}, files, 422),
    (user_data, files, 200),
    ({"username": generate_random_name(7),
     "first_name": "", "last_name": ""}, files, 200),
    ({"username": generate_random_name(10), "first_name": generate_random_name(10),
     "last_name": generate_random_name(10)}, files, 200),
    ({"username": generate_random_name(10), "first_name": generate_random_name(10),
     "last_name": generate_random_name(10)}, {}, 200),

])
def test_get_user_info(client: TestClient, normal_user_token_cookies, input_data: dict, expected_status_code: int, files: dict):
    response = client.put(
        "/users/me", cookies=normal_user_token_cookies, data=input_data, files=files)
    print(response.json())
    assert response.status_code == expected_status_code
