from fastapi import Response, status, HTTPException, Query, APIRouter
from ..database import SessionDependency
from .. import schemas
from typing import Annotated
from sqlmodel import select
from ..models import Post

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/")
def get_posts(
    session: SessionDependency,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> list[schemas.PostResponse]:
    posts = session.exec(select(Post).offset(offset).limit(limit)).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(
    session: SessionDependency,
    post: schemas.PostCreate
    ) -> dict:
    db_post = Post(**post.model_dump())
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(
    session: SessionDependency,
    id: int
    ) -> dict:
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@router.delete("/{id}", response_model=schemas.PostResponse)
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


@router.put("/{id}", response_model=schemas.PostResponse)
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

