from app import schemas
from .database import client, session
import pytest
import jwt
from app.config import settings

@pytest.fixture(autouse=True)
def test_user(client):
    user_data = {"email": "for12@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user


def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "data@works.com", "password": "testpassword"},
    )
    new_user = schemas.UserResponse(**response.json())
    assert response.status_code == 201
    assert new_user.email == "data@works.com"


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user['email'], "password": test_user['password']},
    )
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert response.status_code == 200
    assert login_response.access_token
    assert login_response.token_type == "bearer"