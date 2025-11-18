from fastapi import Response, status, HTTPException, Query, APIRouter
from ..database import SessionDependency
from .. import schemas, oauth2
from typing import Annotated, Optional
from sqlmodel import select
from ..models import Post, Votes
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/")
def get_posts(
    session: SessionDependency,
    current_user: oauth2.OauthDependency,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    search: Optional[str] = ""
    ) -> list[schemas.PostOut]:
    #query = select(Post).where(Post.user_id == current_user.id)

    query = select(Post, func.count(Votes.post_id).label("votes")).join(Votes, Votes.post_id == Post.id, isouter=True).group_by(Post.id)
    
    if search:
        query = query.where(Post.title.contains(search))
    posts = session.exec(query.offset(offset).limit(limit)).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(
    session: SessionDependency,
    post: schemas.PostCreate,
    current_user: oauth2.OauthDependency
    ) -> dict:
    db_post = Post(user_id=current_user.id, **post.model_dump())
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    session: SessionDependency,
    current_user: oauth2.OauthDependency,
    id: int
    ) -> dict:
    post = session.exec(select(Post, func.count(Votes.post_id).label("votes")).join(Votes, Votes.post_id == Post.id, isouter=True).where(Post.id == id).group_by(Post.id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@router.delete("/{id}", response_model=schemas.PostResponse)
def delete_post(
    session: SessionDependency,
    current_user: oauth2.OauthDependency,
    id: int
    ) -> dict:
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    session.delete(post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    session: SessionDependency,
    current_user: oauth2.OauthDependency,
    id: int,
    post: schemas.PostUpdate
    ):
    existing_post = session.get(Post, id)
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if existing_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    dic_post = post.model_dump(exclude_unset=True)
    existing_post.sqlmodel_update(dic_post)
    session.add(existing_post)
    session.commit()
    session.refresh(existing_post)
    
    return existing_post

