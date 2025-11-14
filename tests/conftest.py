from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import Session, SQLModel, create_engine
from app.database import get_session
import os
from dotenv import load_dotenv
import pytest
from app.oauth2 import create_access_token
from app.models import Post

load_dotenv(dotenv_path=".env.dev")

postgresql_url = os.getenv("POSTGRESQL_URL_DEV")
engine = create_engine(postgresql_url)

client = TestClient(app)

@pytest.fixture()
def session():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture()
def client(session):
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def test_user(client):
    user_data = {"email": "for12@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user

@pytest.fixture(autouse=True)
def test_user2(client):
    user_data = {"email": "moon12@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user

@pytest.fixture()
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})


@pytest.fixture()
def authorized_client(client, token):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture()
def test_posts(test_user, test_user2, session):

    posts_data = [
        {"title": "First Post", "content": "Content of first post", "user_id": test_user['id']},
        {"title": "Second Post", "content": "Content of second post", "user_id": test_user['id']},
        {"title": "Third Post", "content": "Content of third post", "user_id": test_user['id']},
        {"title": "Fourth Post", "content": "Content of fourth post", "user_id": test_user2['id']},
        {"title": "Fifth Post", "content": "Content of fifth post", "user_id": test_user2['id']},
    ]
    posts = []
    for post_data in posts_data:
        post = Post(**post_data)
        posts.append(post)
    session.add_all(posts)
    session.commit()
    return posts


