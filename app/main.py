from fastapi import FastAPI, Response, status, HTTPException, Query
from pydantic import BaseModel
from random import randrange
from .database import create_db_and_tables, SessionDependency
import os 
import time
from supabase import create_client, Client
import dotenv
from contextlib import asynccontextmanager
from typing import Annotated, Optional
from sqlmodel import select, Session
from datetime import datetime, timezone
from .models import Post, User
from . import schemas, utils
from .schemas import PostCreate, PostUpdate





dotenv.load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db_and_tables()
        print("🛠️ Database and tables created successfully")
    except Exception as e:
        print(f"Error creating database and tables: {e}")
    yield

    print("🛠️ Application shutting down...")



    
app = FastAPI(lifespan=lifespan)

while True: 
    try:
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        supabase: Client = create_client(url, key)
        print("Supabase client created successfully")
        break
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        time.sleep(4)




@app.get("/")
async def read_root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
def get_posts(
    session: SessionDependency,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> list[schemas.PostResponse]:
    posts = session.exec(select(Post).offset(offset).limit(limit)).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(
    session: SessionDependency,
    post: schemas.PostCreate
    ) -> dict:
    db_post = Post(**post.model_dump())
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(
    session: SessionDependency,
    id: int
    ) -> dict:
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@app.delete("/posts/{id}", response_model=schemas.PostResponse)
def delete_post(
    session: SessionDependency,
    id: int
    ) -> dict:
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    session.delete(post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(
    session: SessionDependency,
    id: int,
    post: schemas.PostUpdate
    ):
    existing_post = session.get(Post, id)
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    dic_post = post.model_dump(exclude_unset=True)
    existing_post.sqlmodel_update(dic_post)
    session.add(existing_post)
    session.commit()
    session.refresh(existing_post)
    
    return existing_post


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(
    session: SessionDependency,
    user: schemas.UserCreate
    ) -> dict:

    user.password = utils.hash(user.password)

    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(
    session: SessionDependency,
    id: int
    ) -> dict:
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(
    session: SessionDependency,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> list[schemas.UserResponse]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@app.delete("/users/{id}", response_model=schemas.UserResponse)
def delete_user(
    session: SessionDependency,
    id: int
    ) -> dict:
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    session.delete(user)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/users/{id}", response_model=schemas.UserResponse)
def update_user(
    session: SessionDependency,
    id: int,
    user: schemas.UserUpdate
    ):

    user.password = utils.hash(user.password)

    existing_user = session.get(User, id)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    dic_user = user.model_dump(exclude_unset=True)
    existing_user.sqlmodel_update(dic_user)
    session.add(existing_user)
    session.commit()
    session.refresh(existing_user)

    return existing_user