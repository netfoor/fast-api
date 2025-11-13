from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import Session, SQLModel, create_engine
from app.database import get_session
import os
from dotenv import load_dotenv
import pytest

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
