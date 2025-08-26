from fastapi import Response, status, HTTPException, Query, APIRouter
from ..database import SessionDependency
from .. import schemas
from typing import Annotated
from sqlmodel import select
from .. import utils
from ..models import User

router = APIRouter(
    prefix="/users"
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
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


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(
    session: SessionDependency,
    id: int
    ) -> dict:
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/", response_model=list[schemas.UserResponse])
def get_users(
    session: SessionDependency,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> list[schemas.UserResponse]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.delete("/{id}", response_model=schemas.UserResponse)
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


@router.put("/{id}", response_model=schemas.UserResponse)
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