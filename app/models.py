from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from sqlalchemy import text
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(primary_key=True, nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    posts: list["Post"] = Relationship(back_populates="owner")
    created_at: datetime | None = Field(
        nullable=False,
        default=datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": text("now()")}
    )


class Post(SQLModel, table=True):
    __tablename__ = "posts"
    id: int = Field(primary_key=True, nullable=False)
    user_id: int = Field(foreign_key="users.id", nullable=False, ondelete="CASCADE")
    title: str = Field(max_length=100, nullable=False)
    content: str = Field(nullable=False)
    published: bool | None = Field(
        nullable=False,
        default=True,
        sa_column_kwargs={"server_default": "true"}
    )
    created_at: datetime | None = Field(
        nullable=False,
        default=datetime.now(timezone.utc), 
        sa_column_kwargs={"server_default": text("now()")}
    )
    owner: Optional["User"] = Relationship(back_populates="posts")

