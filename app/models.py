from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from sqlalchemy import text


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

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(primary_key=True, nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime | None = Field(
        nullable=False,
        default=datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": text("now()")}
    )
