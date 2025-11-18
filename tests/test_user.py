from app import schemas
import jwt, pytest
from app.config import settings

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

@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("nonexistent@user.com", "password123", 404),
        ("for12@gmail.com", "wrongpassword", 401),
        (None, "password123", 404),
        ("for12@gmail.com", None, 401),
    ]
)
def test_login_user_incorrect(client, email, password, status_code):
    response = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == status_code
    
