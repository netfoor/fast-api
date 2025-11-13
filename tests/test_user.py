from app import schemas
from .database import client, session


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}

def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "data@works.com", "password": "testpassword"},
    )
    new_user = schemas.UserResponse(**response.json())
    assert response.status_code == 201
    assert new_user.email == "data@works.com"