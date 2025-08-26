import dotenv
import os
from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends

dotenv.load_dotenv()


# Postgres Engine

postgresql_url = os.environ.get("POSTGRESQL_URL")
engine = create_engine(postgresql_url)

# Create the database and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency
def get_session():
    with Session(engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]
