from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}

def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    new_user = schemas.UserResponse(**response.json())
    assert response.status_code == 201
    assert new_user.email == "test@example.com"